from rest_framework.permissions import BasePermission


class IsRelatedToUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True

        if obj.created_by == request.user:
            return True

        if obj.loan.created_by == request.user:
            return True

        return False
