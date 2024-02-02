import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from core.models import Loan, Payment
from datetime import date


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    pass


@pytest.fixture(scope="session", autouse=True)
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        user1 = User.objects.create_user(
            username="testuser1", password="matera123")
        user2 = User.objects.create_user(
            username="testuser2", password="matera123")

        loan1 = Loan.objects.create(
            nominal_value=1000,
            interest_rate=1,
            ip_address="192.168.0.1",
            request_date=date(2022, 2, 1),
            bank="Banco 1",
            user=user1)
        loan2 = Loan.objects.create(
            nominal_value=2000,
            interest_rate=2,
            ip_address="192.168.0.2",
            request_date=date(2022, 2, 2),
            bank="Banco 2",
            user=user1)
        Loan.objects.create(
            nominal_value=3000,
            interest_rate=3,
            ip_address="192.168.0.3",
            request_date=date(2022, 2, 3),
            bank="Banco 3",
            user=user2)

        Payment.objects.create(
            date=date(2022, 2, 1),
            value=100,
            loan=loan1,
            user=user1)
        Payment.objects.create(
            date=date(2022, 2, 1),
            value=200,
            loan=loan1,
            user=user1)
        Payment.objects.create(
            date=date(2022, 2, 1),
            value=300,
            loan=loan2,
            user=user1)
        Payment.objects.create(
            date=date(2022, 2, 1),
            value=300,
            loan=loan2,
            user=user1)
