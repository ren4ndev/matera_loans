from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from .models import Loan, Payment
from .serializers import LoanSerializer, PaymentSerializer
from .permissions import IsOwnerOrAdmin


class LoanViewSet(viewsets.ModelViewSet):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsOwnerOrAdmin]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Loan.objects.all().prefetch_related("payments")
        else:
            return Loan.objects.filter(user=self.request.user)


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsOwnerOrAdmin]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Payment.objects.all()
        else:
            return Payment.objects.filter(user=self.request.user)
