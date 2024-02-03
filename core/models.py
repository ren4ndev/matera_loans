from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal


class Loan(models.Model):
    nominal_value = models.DecimalField(max_digits=10, decimal_places=2)
    interest_rate = models.DecimalField(max_digits=10, decimal_places=2)
    ip_address = models.CharField(max_length=100)
    request_date = models.DateField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    bank = models.CharField(max_length=100)
    client = models.CharField(max_length=100)

    def calculate_outstanding_balance(self):
        # pro rata die
        payments = self.payments.all().order_by('date')
        interest_per_day = self.interest_rate / 365
        outstanding_balance = self.nominal_value

        # Itera sobre todos pagamentos
        for payment in payments:
            days_since_loan_start = (payment.date - self.request_date).days

            interest_rate_in_period = interest_per_day * Decimal(days_since_loan_start)

            interest_amount = outstanding_balance * interest_rate_in_period

            amortization_amount = payment.value - round(interest_amount, 2)

            outstanding_balance -= amortization_amount

        return outstanding_balance


class Payment(models.Model):
    date = models.DateField()
    value = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    loan = models.ForeignKey(
        Loan, on_delete=models.CASCADE, related_name="payments")
