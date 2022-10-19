from rest_framework import permissions


class AdminOrCriticPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == "GET":
            return True

        return bool(request.user.is_authenticated and request.user.is_superuser or request.user.is_critic)


class AdminOrOwnCriticPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True

        return bool(request.user.is_authenticated and request.user.is_critic and request.user == obj)