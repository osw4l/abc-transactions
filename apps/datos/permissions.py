from rest_framework.permissions import BasePermission


class IsCustomUser(BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user, 'customuser')
