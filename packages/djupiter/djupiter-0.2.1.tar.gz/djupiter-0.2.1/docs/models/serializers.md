# Serializers

Usage guide in progress...

```py
from drf_extra_fields.fields import Base64ImageField as ImageField, Base64FileField as FileField

class ErrorDetailSerializer(serializers.Serializer): pass

class GenericDetailSerializer(serializers.Serializer): pass

class Base64ImageField(ImageField): pass

class Base64FileField(FileField): pass

class UserCredentialsSerializer(serializers.Serializer): pass

class UserSerializer(serializers.ModelSerializer): pass

class TokenSerializer(serializers.Serializer): pass

class EmailSerializer(serializers.Serializer): pass

class EmailWithCodeSerializer(EmailSerializer): pass

class PasswordChangeWithEmailAndCodeSerializer(EmailWithCodeSerializer): pass

class PasswordChangeWithEmailAndCodeErrorsSerializer(serializers.Serializer): pass

class UserSettingsSerializer(serializers.ModelSerializer): pass

class ChangePasswordSerializer(serializers.ModelSerializer): pass

class UserSettingsErrorsSerializer(serializers.Serializer): pass

class RegistrationSerializer(serializers.Serializer): pass

class VerifyConfirmationCodeSerializer(serializers.Serializer): pass
```
