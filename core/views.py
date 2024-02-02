from rest_framework import generics, viewsets
from rest_framework.authentication import TokenAuthentication

from .models import Loan, Payment
from .serializers import UserSerializer, LoanSerializer, PaymentSerializer
from .permissions import IsRelatedToUser


class UserCreate(generics.CreateAPIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = UserSerializer


class LoanViewSet(viewsets.ModelViewSet):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsRelatedToUser]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Loan.objects.all()
        else:
            return Loan.objects.filter(created_by=self.request.user)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsRelatedToUser]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Payment.objects.all()
        else:
            return Payment.objects.filter(
                loan__created_by=self.request.user)
