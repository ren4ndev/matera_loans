from django.contrib.auth.models import User
from core.models import Loan, Payment
from datetime import date


def test_user_table_is_healthy():
    number_of_users = len(User.objects.all())
    assert number_of_users == 2

    User.objects.create(username="testuser3", password="matera123")
    number_of_users = len(User.objects.all())
    assert number_of_users == 3

    user = User.objects.get(id=3)
    user.delete()
    number_of_users = len(User.objects.all())
    assert number_of_users == 2


def test_loan_table_is_healthy():
    number_of_loans = len(Loan.objects.all())
    assert number_of_loans == 3

    user = User.objects.get(id=1)
    Loan.objects.create(
        nominal_value=1000,
        interest_rate=1,
        ip_address="192.168.0.1",
        request_date=date(2022, 2, 1),
        bank="Banco 1",
        client="Client 1",
        created_by=user)
    number_of_loans = len(Loan.objects.all())
    assert number_of_loans == 4

    loan = Loan.objects.get(id=4)
    loan.delete()
    number_of_loans = len(Loan.objects.all())
    assert number_of_loans == 3


def test_payment_table_is_healthy():
    number_of_payments = len(Payment.objects.all())
    assert number_of_payments == 4

    loan = Loan.objects.get(id=1)
    Payment.objects.create(
        date=date(2022, 2, 1),
        value=300,
        loan=loan)
    number_of_payments = len(Payment.objects.all())
    assert number_of_payments == 5

    payment = Payment.objects.get(id=5)
    payment.delete()
    number_of_payments = len(Payment.objects.all())
    assert number_of_payments == 4
