from django.db import models
from django.contrib.auth.models import User


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


class Payment(models.Model):
    date = models.DateField()
    value = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    loan = models.ForeignKey(
        Loan, on_delete=models.CASCADE, related_name="payments")
