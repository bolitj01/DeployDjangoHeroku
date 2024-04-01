from rest_framework import permissions

class IsOwnerOrAdmin(permissions.BasePermission):
    # Called on every request to the view
    def has_permission(self, request, view):
        # Allow all authenticated GET requests at the view level
        if (request.method in ['GET', 'POST', 'PUT', 'DELETE'] 
            and request.user.is_authenticated):
            return True # Moves on to the object level permission
        return False
    # obj is a model instance of Todo
    def has_object_permission(self, request, view, obj):
        # Allow object interaction if the user is the owner or a superuser
        return obj.user == request.user or request.user.is_superuser
