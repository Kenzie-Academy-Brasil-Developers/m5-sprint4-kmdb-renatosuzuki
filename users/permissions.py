from rest_framework import permissions


class AdmPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.is_authenticated and request.user.is_superuser)


class UserPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.is_authenticated)

    
    def has_object_permission(self, request, view, obj):
        return bool(request.user.is_critic and obj.id == request.user.id)