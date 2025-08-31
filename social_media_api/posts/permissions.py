from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Allow full access only to the object's owner (author). Read for others.
    """

    def has_permission(self, request, view):
        # allow list/create for authenticated users; read-only for unauthenticated
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True
        # Write permissions only to owner
        return getattr(obj, 'author', None) == request.user

from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Only owners of an object can edit/delete it.
    """

    def has_object_permission(self, request, view, obj):
        # SAFE_METHODS = GET, HEAD, OPTIONS → always allow
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user
