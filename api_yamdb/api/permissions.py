from rest_framework.permissions import (
    SAFE_METHODS,
    BasePermission,
    IsAuthenticatedOrReadOnly
)

from users.models import UserRoles


class IsAdminRole(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_superuser
            or request.auth and request.user.is_admin
        )


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or request.user.is_superuser
            or request.auth and request.user.role == UserRoles.ADMIN
        )


class IsStaffOrOwnerOrReadOnly(IsAuthenticatedOrReadOnly):
    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (request.method in SAFE_METHODS
                or obj.author == request.user
                or request.user.role in [UserRoles.ADMIN, UserRoles.MODERATOR])
