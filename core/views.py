from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework import status
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

    def perform_create(self, serializer):
        user = self.request.user

        serializer.save(user=user)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


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

    def perform_create(self, serializer):
        user = self.request.user
        loan = serializer.validated_data.get("loan", None)

        serializer.save(user=user, loan=loan)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
