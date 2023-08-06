from rest_framework import serializers

from djupiter.models import User, ConfirmationCode

from drf_extra_fields.fields import Base64ImageField as ImageField, Base64FileField as FileField
from rest_framework import serializers


class ErrorDetailSerializer(serializers.Serializer):
    error = serializers.CharField(max_length=255)


class GenericDetailSerializer(serializers.Serializer):
    detail = serializers.CharField(max_length=255)


class Base64ImageField(ImageField):
    class Meta:
        swagger_schema_fields = {
            'type': 'string',
            'read_only': False,
        }


class Base64FileField(FileField):
    ALLOWED_TYPES = ['pdf']

    class Meta:
        swagger_schema_fields = {
            'type': 'string',
            'read_only': False,
        }

    def get_file_extension(self, filename, decoded_file):
        return 'pdf'



class UserCredentialsSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=25)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['password', 'groups', 'user_permissions']


class TokenSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=255)


class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()


class EmailWithCodeSerializer(EmailSerializer):
    code = serializers.CharField(max_length=4)


class PasswordChangeWithEmailAndCodeSerializer(EmailWithCodeSerializer):
    password1 = serializers.CharField(min_length=8)
    password2 = serializers.CharField(min_length=8)

    def validate(self, data):
        if data["password1"] != data["password2"]:
            raise serializers.ValidationError({"password2": "Passwords must match."})

        return data


class PasswordChangeWithEmailAndCodeErrorsSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)
    code = serializers.CharField(max_length=255)
    password1 = serializers.CharField(max_length=255)
    password2 = serializers.CharField(max_length=255)


class UserSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "phone", "address", "city", "state", "zip")

    def save(self):
        for k, v in self.validated_data.items():
            setattr(self.instance, k, v)

        self.instance.save()
        return self.instance


class ChangePasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("old_password", "password1", "password2",)

    old_password = serializers.CharField(min_length=8, max_length=25, required=False)
    password1 = serializers.CharField(min_length=8, max_length=25, required=False)
    password2 = serializers.CharField(min_length=8, max_length=25, required=False)

    def validate(self, data):
        if not self.instance.check_password(data["old_password"]):
            raise serializers.ValidationError({"old_password": "Incorrect password."})

        if data["password1"] != data["password2"]:
            raise serializers.ValidationError({"password2": "Passwords must match."})

        return data

    def save(self):
        self.instance.set_password(self.validated_data["password1"])
        self.instance.save()

        return self.instance

    def to_representation(self, instance):
        return UserSerializer(instance=instance).data


class UserSettingsErrorsSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=25)
    last_name = serializers.CharField(max_length=25)
    email = serializers.CharField(max_length=25)
    phone = serializers.CharField(max_length=25)
    address = serializers.CharField(max_length=25)
    city = serializers.CharField(max_length=25)
    state = serializers.CharField(max_length=25)
    zip = serializers.CharField(max_length=25)


class RegistrationSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=25)
    last_name = serializers.CharField(max_length=25)
    email = serializers.EmailField()
    phone = serializers.CharField(max_length=25)
    password1 = serializers.CharField(min_length=8, max_length=25)
    password2 = serializers.CharField(min_length=8, max_length=25)

    def validate_email(self, value):
        if User.objects.filter(email=value):
            raise serializers.ValidationError("Email already exists.")
        return value

    def validate(self, data):
        if data["password1"] != data["password2"]:
            raise serializers.ValidationError({"password2": "Passwords must match."})

        return data

    def create(self, validated_data):
        password, _ = validated_data.pop("password1"), validated_data.pop("password2")
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()

        return user


class VerifyConfirmationCodeSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=4)

    def validate(self, data):
        try:
            user = User.objects.get(email=data["email"])
            code = ConfirmationCode.objects.get(user=user, code=data["code"])
            if code.has_expired:
                raise serializers.ValidationError({"code": "Code has already expired."})

        except (ConfirmationCode.DoesNotExist, User.DoesNotExist):
            raise serializers.ValidationError({"code": "Invalid code."})

        return data

    def create(self, validated_data):
        user = User.objects.get(email=validated_data["email"])
        user.is_email_confirmed = True
        user.save()
        user.confirmation_code.delete()

        return user
