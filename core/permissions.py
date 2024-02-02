from rest_framework.permissions import BasePermission


class IsRelatedToUser(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Verifica se o usuário é um superusuário
        if request.user.is_superuser:
            return True

        # Verifica se o usuário é o dono direto do objeto
        if obj.created_by == request.user:
            return True

        # Verifica se o empréstimo associado ao pagamento pertence ao usuário
        if obj.loan.created_by == request.user:
            return True

        return False
