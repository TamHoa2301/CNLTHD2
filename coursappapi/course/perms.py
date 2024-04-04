from rest_framework import permissions

class CreateOwner(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, comment):
        return super().has_permission(request, view) and request.user == comment.user