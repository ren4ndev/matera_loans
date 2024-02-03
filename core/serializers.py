from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

from .models import Loan, Payment


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "email", "password")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User(
            email=validated_data["email"],
            username=validated_data["username"]
        )
        user.set_password(validated_data["password"])
        user.save()
        Token.objects.create(user=user)
        return user


class PaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = "__all__"


class LoanSerializer(serializers.ModelSerializer):
    payments = PaymentSerializer(many=True, read_only=True, required=False)
    outstanding_balance = serializers.SerializerMethodField()

    class Meta:
        model = Loan
        fields = "__all__"
        read_only_fields = ('created_by',)

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super(LoanSerializer, self).create(validated_data)

    def get_outstanding_balance(self, obj):
        outstanding_balance = obj.calculate_outstanding_balance()
        return outstanding_balance
