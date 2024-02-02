from rest_framework import generics, viewsets
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth import authenticate

from .models import Loan, Payment
from .serializers import UserSerializer, LoanSerializer, PaymentSerializer
from .permissions import IsRelatedToUser


class UserCreate(generics.CreateAPIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = UserSerializer


class LoginView(APIView):
    permission_classes = ()

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        if user:
            return Response({"token": user.auth_token.key})
        else:
            return Response(
                {"error": "Wrong Credentials"},
                status=status.HTTP_400_BAD_REQUEST)


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
