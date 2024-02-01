from rest_framework import serializers
from .models import Loan, Payment


class LoanSerializer(serializers.HyperlinkedModelSerializer):
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
    class Meta:
        model = Payment
        fields = [
            "id",
            "date",
            "value",
            "loan",
        ]
