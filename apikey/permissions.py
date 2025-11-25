from rest_framework import permissions
from .models import APIKey

class HasAPIKey(permissions.BasePermission):
    """
    Permite acesso apenas se uma API Key válida foi fornecida na autenticação.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and isinstance(request.user, APIKey))