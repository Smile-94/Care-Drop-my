# permissions.py
from rest_framework.permissions import BasePermission

class OwnProfilePermission(BasePermission):
    """
    Object-level permission to only allow updating his own profile
    """
    def has_object_permission(self, request, view, obj):
        # Allow read access to any user
        if request.method in BasePermission.SAFE_METHODS:
            return True

        # Allow write access only to owner of the profile
        return obj.email == request.user.email