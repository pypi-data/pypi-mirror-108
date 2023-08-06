from rest_framework import permissions


class IsEmailConfirmed(permissions.BasePermission):
    message = "You must confirm your email first."

    def has_permission(self, request, view):
        return request.user.is_email_confirmed
