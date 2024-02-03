from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth.models import User
from datetime import date

from core.models import Loan, Payment


class PaymentAPITest(APITestCase):
    def setUp(self):
        self.url = "/payments/"

        self.user1 = User.objects.create_user(username='testuser1', password='testpassword1')
        self.client1 = APIClient()
        self.client1.force_authenticate(user=self.user1)
        self.loan1 = Loan.objects.create(
            nominal_value=1000,
            interest_rate=1,
            ip_address="192.168.0.1",
            request_date=date(2022, 2, 1),
            bank="Banco 1",
            client="Client 1",
            created_by=self.user1)
        self.payment1_user1 = Payment.objects.create(
            date=date(2022, 2, 1),
            value=100,
            loan=self.loan1)
        self.payment2_user1 = Payment.objects.create(
            date=date(2022, 2, 1),
            value=200,
            loan=self.loan1)

        self.user2 = User.objects.create_user(username='testuser2', password='testpassword2')
        self.client2 = APIClient()
        self.client2.force_authenticate(user=self.user2)
        self.loan2 = Loan.objects.create(
            nominal_value=2000,
            interest_rate=2,
            ip_address="192.168.0.2",
            request_date=date(2022, 2, 2),
            bank="Banco 2",
            client="Client 2",
            created_by=self.user2)
        self.payment1_user2 = Payment.objects.create(
            date=date(2022, 2, 1),
            value=300,
            loan=self.loan2)

    def tearDown(self):
        Loan.objects.all().delete()
        Payment.objects.all().delete()

    def test_authenticaded_user_can_get_payment_list(self):
        url = self.url
        response = self.client1.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_authenticaded_user_cannot_get_other_users_payment_list(self):
        url = self.url
        response = self.client2.get(url)
        first_payment = response.data[0]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(Payment.objects.all()), 3)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(first_payment["value"], "300.00")

    def test_unauthenticaded_user_cannot_get_payment_list(self):
        self.client1.logout()

        url = self.url
        response = self.client1.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authenticated_user_can_create_payment(self):
        url = self.url
        data = {
            "date": "2024-02-01",
            "value": "140.00",
            "loan": self.loan1.id
        }
        response = self.client1.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["value"], "140.00")
        self.assertEqual(response.data["loan"], self.loan1.id)
        self.assertEqual(len(Payment.objects.all()), 4)

    def test_unauthenticated_user_cannot_create_payment(self):
        self.client1.logout()

        url = self.url
        data = {
            "date": "2024-02-01",
            "value": "140.00",
            "loan": self.loan1.id
        }
        response = self.client1.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authenticated_user_can_update_payment(self):
        url = f'{self.url}{self.payment1_user1.id}/'
        data = {
            "date": "2024-02-01",
            "value": "500.00",
            "loan": self.loan1.id
        }
        response = self.client1.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        updated_payment = Payment.objects.get(id=self.payment1_user1.id)
        self.assertEqual(updated_payment.value, 500.00)

    def test_authenticated_user_cannot_update_other_users_payment(self):
        url = f'{self.url}{self.payment1_user2.id}/'
        data = {
            "date": "2024-02-01",
            "value": "500.00",
            "loan": self.loan2.id
        }
        response = self.client1.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        updated_payment = Payment.objects.get(id=self.payment1_user2.id)
        self.assertEqual(updated_payment.value, 300.00)

    def test_unauthenticated_user_cannot_update_payment(self):
        self.client1.logout()

        url = f'{self.url}{self.payment1_user1.id}/'
        data = {
            "date": "2024-02-01",
            "value": "500.00",
            "loan": self.loan1.id
        }
        response = self.client1.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        payment = Payment.objects.get(id=self.payment1_user1.id)
        self.assertEqual(payment.value, 100.00)

    def test_authenticated_user_can_delete_payment(self):
        url = f'{self.url}{self.payment1_user1.id}/'

        response = self.client1.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_authenticated_user_cannot_delete_others_users_payment(self):
        url = f'{self.url}{self.payment1_user2.id}/'

        response = self.client1.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_unauthenticated_user_cannot_delete_loan(self):
        self.client1.logout()

        url = f'{self.url}{self.payment1_user1.id}/'

        response = self.client1.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
