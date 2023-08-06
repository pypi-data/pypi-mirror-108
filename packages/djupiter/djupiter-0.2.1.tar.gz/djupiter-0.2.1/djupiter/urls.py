from django.urls import path, re_path
from django.conf import settings

from djupiter import views
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

app_name = "djupiter"

schema_view = get_schema_view(
    openapi.Info(
        title=f"{settings.PROJECT_NAME} API",
        default_version=f'v{settings.PROJECT_API_VERSION}',
        description=f"ReST API for the {settings.PROJECT_NAME} Project",
        contact=openapi.Contact(email=f"{settings.PROJECT_DEVELOPER_EMAIL}"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)


urlpatterns = [
    re_path(r'^docs/(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^docs/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path("token/login/", views.token_login, name="token-login"),
    path("password/reset/", views.password_reset, name="password-reset"),
    path("password/reset/confirm/", views.password_reset_confirm, name="password-reset-confirm"),
    path("password/reset/change/", views.password_reset_change, name="password-reset-change"),
    path("account-settings/", views.AccountSettingsView.as_view(), name="account-settings"),
    path("change-password/", views.ChangePasswordView.as_view(), name="change-password"),
    path("register/", views.RegistrationView.as_view(), name="register"),
    path("register/confirm/", views.VerifyConfirmationCodeView.as_view(), name="register-confirm"),
    path("register/confirm/resend/", views.ResendConfirmationCodeView.as_view(), name="register-resend"),
    path("me/", views.UserInformationView.as_view(), name="me"),
]
