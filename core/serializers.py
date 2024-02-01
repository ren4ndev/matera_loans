from rest_framework import serializers
from .models import Loan, Payment


class LoanSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        read_only=True, default=serializers.CurrentUserDefault()
    )

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
        ]


class PaymentSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        read_only=True, default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Payment
        fields = [
            "id",
            "date",
            "value",
            "loan",
            "user",
        ]
