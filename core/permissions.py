from rest_framework.permissions import BasePermission
from .models import Loan, Payment


class IsRelatedToUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True

        if isinstance(obj, Loan) and obj.created_by == request.user:
            return True

        if isinstance(obj, Payment) and obj.loan.created_by == request.user:
            return True

        return False
