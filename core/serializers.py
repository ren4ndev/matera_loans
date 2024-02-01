from rest_framework import serializers
from .models import Loan, Payment


class PaymentSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        read_only=True, default=serializers.CurrentUserDefault()
    )
    loan = serializers.PrimaryKeyRelatedField(queryset=Loan.objects.all())

    class Meta:
        model = Payment
        fields = [
            "id",
            "date",
            "value",
            "user",
            "loan"
        ]


class LoanSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        read_only=True, default=serializers.CurrentUserDefault()
    )
    payments = PaymentSerializer(many=True, read_only=True)

    class Meta:
        model = Loan
        fields = [
            "id",
            "nominal_value",
            "interest_rate",
            "ip_address",
            "request_date",
            "bank",
            "user",
            "payments",
        ]
