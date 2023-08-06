import json
from datetime import timedelta

from django.core import mail
from django.urls import reverse
from django.utils import timezone
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from djupiter.factories import SuperAdminFactory, PasswordResetCodeFactory, CommonerFactory
from djupiter.models import PasswordResetCode, User, ConfirmationCode
from djupiter.serializers import UserSettingsSerializer, UserSerializer, GenericDetailSerializer, ErrorDetailSerializer


class DjupiterTest(APITestCase):
    def setUp(self):
        super().setUp()

        self.password = "p@ssword!"

    def test_can_fetch_a_token_with_correct_credentials(self):
        user = SuperAdminFactory()
        user.set_password(self.password)
        user.save()
        payload = {
            "email": user.email,
            "password": self.password
        }

        response = self.client.post(
            reverse("auth:token-login"),
            json.dumps(payload),
            content_type="application/json"
        )

        self.assertEquals({"token": Token.objects.get(user=user).key}, response.data)

    def test_can_email_a_password_reset_code(self):
        user = SuperAdminFactory()
        payload = {"email": user.email}
        response = self.client.post(
            reverse("auth:password-reset"),
            json.dumps(payload),
            content_type="application/json",
        )

        self.assertEquals({"detail": f"We have sent a verification code to your email {user.email}"}, response.data)

        code = PasswordResetCode.objects.filter(user=user).last()
        self.assertIn(str(code), mail.outbox[0].body)

    def test_will_not_send_an_email_for_nonexistent_accounts(self):
        nonexistent_email = "jdoe@example.com"
        payload = {"email": nonexistent_email}
        response = self.client.post(
            reverse("auth:password-reset"),
            json.dumps(payload),
            content_type="application/json",
        )

        # The response is the same to prevent leaking email data.
        self.assertEquals({"detail": f"We have sent a verification code to your email {nonexistent_email}"},
                          response.data)

        self.assertEquals(0, PasswordResetCode.objects.count())
        self.assertEquals(0, len(mail.outbox))

    def test_can_confirm_if_a_password_reset_code_is_valid(self):
        user = SuperAdminFactory()
        code = PasswordResetCodeFactory(user=user)

        payload = {"email": user.email, "code": str(code)}
        response = self.client.post(
            reverse("auth:password-reset-confirm"),
            json.dumps(payload),
            content_type="application/json",
        )

        self.assertEquals(200, response.status_code)
        self.assertEquals(GenericDetailSerializer({"detail": "The code is valid."}).data, response.data)

    def test_will_error_if_the_password_reset_code_is_invalid(self):
        user = SuperAdminFactory()
        code = PasswordResetCodeFactory(user=user, code="1234")

        payload = {"email": user.email, "code": "abcd"}
        response = self.client.post(
            reverse("auth:password-reset-confirm"),
            json.dumps(payload),
            content_type="application/json",
        )

        self.assertEquals(401, response.status_code)
        self.assertEquals(ErrorDetailSerializer({"error": "The code is invalid."}).data, response.data)

    def test_will_error_if_the_password_reset_code_has_expired(self):
        user = SuperAdminFactory()
        code = PasswordResetCodeFactory(user=user, expires_at=timezone.now() - timedelta(minutes=30))

        payload = {"email": user.email, "code": str(code)}
        response = self.client.post(
            reverse("auth:password-reset-confirm"),
            json.dumps(payload),
            content_type="application/json",
        )

        self.assertEquals(410, response.status_code)
        self.assertEquals(ErrorDetailSerializer({"error": "The code has expired."}).data, response.data)

    def test_can_change_password_using_password_reset_code(self):
        user = SuperAdminFactory()
        code = PasswordResetCodeFactory(user=user)
        other_codes = PasswordResetCodeFactory.create_batch(3, user=user)

        payload = {"email": user.email, "code": str(code), "password1": "new-password", "password2": "new-password"}
        response = self.client.post(
            reverse("auth:password-reset-change"),
            json.dumps(payload),
            content_type="application/json",
        )

        self.assertEquals(200, response.status_code)
        self.assertEquals(GenericDetailSerializer({"detail": "Password successfully changed."}).data, response.data)

        # All password reset codes of the user are then deleted
        self.assertFalse(PasswordResetCode.objects.filter(user=user, code=str(code)))

    def test_will_error_when_changing_password_if_the_password_reset_code_is_invalid(self):
        user = SuperAdminFactory()
        PasswordResetCodeFactory(user=user, code="1234")

        payload = {"email": user.email, "code": "abcd", "password1": "new-password", "password2": "new-password"}
        response = self.client.post(
            reverse("auth:password-reset-change"),
            json.dumps(payload),
            content_type="application/json",
        )

        self.assertEquals(401, response.status_code)
        self.assertEquals(ErrorDetailSerializer({"error": "The code is invalid."}).data, response.data)

    def test_will_error_when_changing_pasword_if_the_password_reset_code_has_expired(self):
        user = SuperAdminFactory()
        code = PasswordResetCodeFactory(user=user, expires_at=timezone.now() - timedelta(minutes=30))

        payload = {"email": user.email, "code": str(code), "password1": "new-password", "password2": "new-password"}
        response = self.client.post(
            reverse("auth:password-reset-change"),
            json.dumps(payload),
            content_type="application/json",
        )

        self.assertEquals(410, response.status_code)
        self.assertEquals(ErrorDetailSerializer({"error": "The code has expired."}).data, response.data)

    def test_can_fetch_a_users_account_settings(self):
        user = SuperAdminFactory()
        token = Token.objects.create(user=user)

        response = self.client.get(reverse("auth:account-settings"), HTTP_AUTHORIZATION="Token " + str(token))

        self.assertEquals(200, response.status_code)
        self.assertEquals(UserSettingsSerializer(instance=user).data, response.data)

    def test_can_update_a_users_account_settings(self):
        user = SuperAdminFactory()
        token = Token.objects.create(user=user)

        payload = json.dumps({
            "first_name": "John",
            "last_name": "Doe",
            "email": "jdoe@example.com",
            "phone": "+44 22661 23",
            "address": "551 3rd Street",
            "city": "South Beach",
            "state": "FL",
            "zip": 554,
        })

        response = self.client.patch(
            reverse("auth:account-settings"),
            payload,
            content_type="application/json",
            HTTP_AUTHORIZATION="Token " + str(token),
        )

        user.refresh_from_db()
        self.assertEquals(200, response.status_code)
        self.assertEquals(UserSettingsSerializer(instance=user).data, response.data)

    def test_omitting_the_password_when_updating_will_not_affect_the_users_credentials(self):
        user = SuperAdminFactory()
        user.set_password("my-password-123")
        user.save()

        token = Token.objects.create(user=user)

        payload = json.dumps({
            "first_name": "John",
            "last_name": "Doe",
            "email": "jdoe@example.com",
            "phone": "+44 22661 23",
            "address": "551 3rd Street",
            "city": "South Beach",
            "state": "FL",
            "zip": 554,
            # No password provided
        })

        response = self.client.patch(
            reverse("auth:account-settings"),
            payload,
            content_type="application/json",
            HTTP_AUTHORIZATION="Token " + str(token),
        )

        user.refresh_from_db()
        self.assertEquals(200, response.status_code)
        self.assertEquals(UserSettingsSerializer(instance=user).data, response.data)
        self.assertTrue(user.check_password("my-password-123"))

    def test_can_register_a_user(self):
        payload = json.dumps({
            "first_name": "Chidi",
            "last_name": "Anagonye",
            "email": "chidi@tgp.com",
            "phone": "+123 456 7890",
            "password1": "p@ssword!",
            "password2": "p@ssword!",
        })

        response = self.client.post(
            reverse("auth:register"),
            payload,
            content_type="application/json",
        )

        self.assertEquals(201, response.status_code)
        created_user = User.objects.first()
        self.assertEquals({"detail": f"We have sent a verification code to your email {created_user.email}"},
                          response.data)
        self.assertIn(str(created_user.confirmation_code), mail.outbox[0].body)

    def test_can_verify_a_confirmation_code(self):
        user = CommonerFactory(is_email_confirmed=False)
        code = ConfirmationCode.objects.create(user=user)
        payload = json.dumps({
            "email": user.email,
            "code": str(code),
        })

        response = self.client.post(
            reverse("auth:register-confirm"),
            payload,
            content_type="application/json",
        )

        self.assertEquals(200, response.status_code)
        self.assertEquals({"detail": f"{user.email} has been successfully verified"}, response.data)
        user.refresh_from_db()
        self.assertTrue(user.is_email_confirmed)
        self.assertRaises(ConfirmationCode.DoesNotExist, lambda: user.confirmation_code)

    def test_verification_fails_if_the_code_is_expired(self):
        user = CommonerFactory()
        code = ConfirmationCode.objects.create(user=user, expires_at=timezone.now() - timedelta(minutes=30))
        payload = json.dumps({
            "email": user.email,
            "code": str(code),
        })

        response = self.client.post(
            reverse("auth:register-confirm"),
            payload,
            content_type="application/json",
        )

        self.assertEquals(422, response.status_code)
        self.assertIn("Code has already expired.", response.data["code"])

    def test_verification_fails_if_the_code_is_invalid(self):
        user = CommonerFactory()
        ConfirmationCode.objects.create(user=user, code="ABCD")
        payload = json.dumps({
            "email": user.email,
            "code": "1234",
        })

        response = self.client.post(
            reverse("auth:register-confirm"),
            payload,
            content_type="application/json",
        )

        self.assertEquals(422, response.status_code)
        self.assertIn("Invalid code.", response.data["code"])

    def test_verification_fails_if_the_email_doesnt_exist(self):
        user = CommonerFactory(email="alice@example.com")
        code = ConfirmationCode.objects.create(user=user)
        payload = json.dumps({
            "email": "bob@example.com",
            "code": str(code),
        })

        response = self.client.post(
            reverse("auth:register-confirm"),
            payload,
            content_type="application/json",
        )

        self.assertEquals(422, response.status_code)
        self.assertIn("Invalid code.", response.data["code"])

    def test_can_resend_confirmation_code(self):
        user = CommonerFactory(email="alice@example.com")
        ConfirmationCode.objects.create(user=user)

        payload = json.dumps({"email": user.email})

        response = self.client.post(
            reverse("auth:register-resend"),
            payload,
            content_type="application/json",
        )

        self.assertEquals(200, response.status_code)
        user.refresh_from_db()
        self.assertEquals({"detail": f"We have sent a verification code to your email {user.email}"},
                          response.data)
        self.assertIn(str(user.confirmation_code), mail.outbox[0].body)

    def test_can_change_a_users_password(self):
        user = SuperAdminFactory()
        user.set_password("password-123")
        user.save()
        token = Token.objects.create(user=user)

        payload = json.dumps({
            "old_password": "password-123",
            "password1": "123-password",
            "password2": "123-password",
        })

        response = self.client.patch(
            reverse("auth:change-password"),
            payload,
            content_type="application/json",
            HTTP_AUTHORIZATION="Token " + str(token),
        )

        self.assertEquals(200, response.status_code)
        user.refresh_from_db()
        self.assertTrue(user.check_password("123-password"))

    def test_can_fetch_own_information(self):
        user = SuperAdminFactory()
        token = Token.objects.create(user=user)

        response = self.client.get(
            reverse("auth:me"),
            HTTP_AUTHORIZATION="Token " + str(token),
        )

        self.assertEquals(200, response.status_code)
        self.assertEquals(UserSerializer(instance=user).data, response.data)
