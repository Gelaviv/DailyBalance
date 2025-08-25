from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAuthenticatedOrCreateOnly(BasePermission):
    """
    The request is authenticated as a user, or is a create-only request.
    """
    def has_permission(self, request, view):
        if request.method == 'POST':
            return True
        return request.user and request.user.is_authenticated