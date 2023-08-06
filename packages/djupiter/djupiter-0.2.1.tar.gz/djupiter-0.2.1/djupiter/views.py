from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from django.db import transaction
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.views import APIView

from djupiter.models import PasswordResetCode, User
from djupiter.permissions import IsEmailConfirmed
from djupiter.serializers import (
    UserCredentialsSerializer,
    TokenSerializer,
    EmailSerializer,
    EmailWithCodeSerializer,
    PasswordChangeWithEmailAndCodeSerializer,
    PasswordChangeWithEmailAndCodeErrorsSerializer, UserSettingsSerializer, UserSettingsErrorsSerializer,
    RegistrationSerializer, UserSerializer, ChangePasswordSerializer, VerifyConfirmationCodeSerializer, 
    ErrorDetailSerializer, GenericDetailSerializer
)


@swagger_auto_schema(
    method="POST",
    request_body=UserCredentialsSerializer,
    responses={
        200: TokenSerializer,
        401: ErrorDetailSerializer,
    },
)
@api_view(["POST"])
@transaction.atomic
def token_login(request):
    """
    Provide the user credentials for an access token.
    Use the token by attaching this header `Authentication: Token example-token-123` to access protected resources.
    That means you need to enter `Token example-token-123` (note that the word "Token" is included) when \
    authenticating using Swagger (the lock icon on the right hand side).
    """
    serializer = UserCredentialsSerializer(data=request.data)
    if serializer.is_valid():
        user = authenticate(username=serializer.data["email"], password=serializer.data["password"])

        if user is not None:
            token, _ = Token.objects.get_or_create(user=user)
            update_last_login(None, user)
            return Response(TokenSerializer({"token": str(token)}).data)

    return Response(ErrorDetailSerializer({"error": "Invalid credentials."}).data, status=401)


@swagger_auto_schema(
    method="POST",
    request_body=EmailSerializer,
    responses={
        200: GenericDetailSerializer,
    },
)
@api_view(["POST"])
@transaction.atomic
def password_reset(request):
    """
    Sends a Password Reset Code to the provided email.
    For security purposes, the endpoint will **return the same detail message** whether the email is valid or not.
    """
    email = request.data.get("email")

    try:
        user = User.objects.get(email=email)
        code = PasswordResetCode.objects.create(user=user)
        user.send_password_reset_code(code)

    except User.DoesNotExist:
        pass

    return Response(GenericDetailSerializer({"detail": f"We have sent a verification code to your email {email}"}).data)


@swagger_auto_schema(
    method="POST",
    request_body=EmailWithCodeSerializer,
    responses={
        200: GenericDetailSerializer,
        410: ErrorDetailSerializer,
        401: ErrorDetailSerializer,
    },
)
@api_view(["POST"])
@transaction.atomic
def password_reset_confirm(request):
    """
    Validates if the provided Password Reset Code is attached to the provided email.
    Will return `410` if the code has already expired.`
    """
    code = PasswordResetCode.objects.filter(
        code=request.data.get("code"),
        user__email=request.data.get("email"),
    ).last()

    if code is None:
        return Response(ErrorDetailSerializer({"error": "The code is invalid."}).data, status=401)

    if code.has_expired:
        return Response(ErrorDetailSerializer({"error": "The code has expired."}).data, status=410)

    return Response(GenericDetailSerializer({"detail": "The code is valid."}).data)


@swagger_auto_schema(
    method="POST",
    request_body=PasswordChangeWithEmailAndCodeSerializer,
    responses={
        200: GenericDetailSerializer,
        401: ErrorDetailSerializer,
        410: ErrorDetailSerializer,
        422: PasswordChangeWithEmailAndCodeErrorsSerializer,
    },
)
@api_view(["POST"])
@transaction.atomic
def password_reset_change(request):
    """
    Change the provided email's password using the provided code.
    Upon successfully changing a password, **ALL** previous Password Reset Codes for that email are deleted.
    """
    serializer = PasswordChangeWithEmailAndCodeSerializer(data=request.data)
    code = PasswordResetCode.objects.filter(
        code=request.data.get("code"),
        user__email=request.data.get("email"),
    ).last()

    if code is None:
        return Response(ErrorDetailSerializer({"error": "The code is invalid."}).data, status=401)

    if code.has_expired:
        return Response(ErrorDetailSerializer({"error": "The code has expired."}).data, status=410)

    if serializer.is_valid():
        code.user.set_password(serializer.data.get("password1"))
        code.user.save()
        code.user.password_reset_codes.all().delete()
        return Response({"detail": "Password successfully changed."})

    return Response(serializer.errors, status=422)


class AccountSettingsView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsEmailConfirmed]

    @swagger_auto_schema(responses={200: UserSettingsSerializer})
    @action(detail=False, methods=["GET"])
    @transaction.atomic
    def get(self, request):
        """
        Fetch the current user's account settings.
        The password is omitted from the response body.
        """
        return Response(UserSettingsSerializer(instance=request.user).data)

    @swagger_auto_schema(
        request_body=UserSettingsSerializer,
        responses={
            200: UserSettingsSerializer,
            401: ErrorDetailSerializer,
            422: UserSettingsErrorsSerializer,
        },
    )
    @action(detail=False, methods=["PATCH"])
    @transaction.atomic
    def patch(self, request):
        """
        Update the current user's account settings.
        """
        serializer = UserSettingsSerializer(instance=request.user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=422)


class ChangePasswordView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsEmailConfirmed]

    @swagger_auto_schema(
        request_body=ChangePasswordSerializer,
        responses={
            200: ChangePasswordSerializer,
            401: ErrorDetailSerializer,
        },
    )
    @action(detail=False, methods=["PATCH"])
    @transaction.atomic
    def patch(self, request):
        """
        Change the current user's password.
        """
        serializer = ChangePasswordSerializer(instance=request.user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=422)


class RegistrationView(APIView):
    @swagger_auto_schema(
        request_body=RegistrationSerializer,
        responses={
            201: GenericDetailSerializer,
            401: ErrorDetailSerializer,
        },
    )
    @action(detail=False, methods=["POST"])
    @transaction.atomic
    def post(self, request):
        """
        Register a new account.
        """
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # TODO: Move unnecessary logic to signals
            user.send_confirmation_code()
            return Response({"detail": f"We have sent a verification code to your email {user.email}"}, status=201)

        return Response(serializer.errors, status=422)


class VerifyConfirmationCodeView(APIView):
    @swagger_auto_schema(
        request_body=VerifyConfirmationCodeSerializer,
        responses={
            200: GenericDetailSerializer,
            401: ErrorDetailSerializer,
        },
    )
    @action(detail=False, methods=["POST"])
    @transaction.atomic
    def post(self, request):
        """
        Verifies a confirmation code for an account.
        """
        serializer = VerifyConfirmationCodeSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"detail": f"{user.email} has been successfully verified"}, status=200)

        return Response(serializer.errors, status=422)


class UserInformationView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsEmailConfirmed]

    @swagger_auto_schema(
        responses={
            200: UserSerializer,
            401: ErrorDetailSerializer,
        },
    )
    @action(detail=False, methods=["GET"])
    @transaction.atomic
    def get(self, request):
        """
        Fetch the information of the current user.
        """
        return Response(UserSerializer(instance=request.user).data, status=200)


class ResendConfirmationCodeView(APIView):
    @swagger_auto_schema(
        request_body=EmailSerializer,
        responses={
            200: GenericDetailSerializer,
            401: ErrorDetailSerializer,
        },
    )
    @action(detail=False, methods=["POST"])
    @transaction.atomic
    def post(self, request):
        """
        Resend a confirmation code for an account.
        For security purposes, the endpoint will **return the same detail message** whether the email is valid or not.
        """
        email = request.data.get("email")

        try:
            user = User.objects.get(email=email)
            user.send_confirmation_code()

        except User.DoesNotExist:
            pass

        return Response({"detail": f"We have sent a verification code to your email {email}"})
