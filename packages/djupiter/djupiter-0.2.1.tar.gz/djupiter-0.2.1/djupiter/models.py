from datetime import timedelta

from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.mail import send_mail
from django.db import models
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.crypto import get_random_string

from djupiter.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_email_confirmed = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    avatar = models.ImageField(upload_to="avatars/", null=True, blank=True)
    phone = models.CharField(max_length=255, blank=True)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=255, blank=True)
    state = models.CharField(max_length=255, blank=True)
    zip = models.IntegerField(null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """
        Returns the short name for the user.
        """
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def send_confirmation_code(self):
        """
        Creates a new confirmation code and sends it to the account's email
        """

        # Clear the old one first.
        ConfirmationCode.objects.filter(user=self).delete()
        confirmation_code = ConfirmationCode.objects.create(user=self)

        message = render_to_string("djupiter/email/confirmation.html", {"code": confirmation_code.code})
        return send_mail("Email Confirmation Code", message, settings.EMAIL_FROM, [self.email], html_message=message)

    def send_password_reset_code(self, code):
        """
        Sends an email to this User containing the password reset code.
        """
        # TODO: refactor to mimic the send_confirmation_code
        message = render_to_string("djupiter/email/password-reset-code.html", {"code": code})
        send_mail("Password Reset Code", message, settings.EMAIL_FROM, [self.email], html_message=message)



class SuperAdmin(User):
    class Meta:
        proxy = True
        verbose_name = "Super Admin"
        verbose_name_plural = "Super Admins"


class Commoner(User):
    class Meta:
        proxy = True
        verbose_name = "Commoner"
        verbose_name_plural = "Commoners"


def _generate_code():
    return get_random_string(length=4).upper()


def _30_mins_from_now():
    return timezone.now() + timedelta(minutes=30)


class PasswordResetCode(models.Model):
    user = models.ForeignKey(User, related_name="password_reset_codes", on_delete=models.CASCADE)
    code = models.CharField(max_length=4, default=_generate_code)
    expires_at = models.DateTimeField(default=_30_mins_from_now)

    def __str__(self):
        return self.code

    @property
    def has_expired(self):
        return self.expires_at < timezone.now()


class ConfirmationCode(models.Model):
    class Meta:
        verbose_name = "Confirmation Code"
        verbose_name_plural = "Confirmation Codes"

    user = models.OneToOneField(User, related_name="confirmation_code", null=True, on_delete=models.SET_NULL)
    code = models.CharField(max_length=4, default=_generate_code)
    expires_at = models.DateTimeField(default=_30_mins_from_now)

    def __str__(self):
        return self.code

    @property
    def has_expired(self):
        return self.expires_at < timezone.now()
