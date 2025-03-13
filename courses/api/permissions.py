from rest_framework.permissions import BasePermission


class IsEnrolled(BasePermission):
    """ Check if the user is enrolled in the course """
    def has_object_permission(self, request, view, obj):
        return obj.students.filter(id=request.user.id).exists()
