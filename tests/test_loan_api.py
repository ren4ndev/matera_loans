from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth.models import User
from datetime import date

from core.models import Loan


class LoanAPITest(APITestCase):
    def setUp(self):
        self.url = "/loans/"

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

    def tearDown(self):
        Loan.objects.all().delete()

    def test_authenticaded_user_can_get_loan_list(self):
        url = self.url
        response = self.client1.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_authenticaded_user_cannot_get_other_users_loan_list(self):
        url = self.url
        response = self.client2.get(url)
        first_loan = response.data[0]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(Loan.objects.all()), 2)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(first_loan["nominal_value"], "2000.00")

    def test_unauthenticaded_user_cannot_get_loan_list(self):
        self.client1.logout()

        url = self.url
        response = self.client1.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authenticated_user_can_create_loan(self):
        url = self.url
        data = {
            "nominal_value": "20000.00",
            "interest_rate": "24.00",
            "ip_address": "163.198.0.20",
            "request_date": "2024-02-20",
            "bank": "Sicoob",
            "client": "Ada Lovelace"
        }
        response = self.client1.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["created_by"], self.user1.id)

    def test_unauthenticated_user_cannot_create_loan(self):
        self.client1.logout()

        url = self.url
        data = {
            "nominal_value": "20000.00",
            "interest_rate": "24.00",
            "ip_address": "163.198.0.20",
            "request_date": "2024-02-20",
            "bank": "Sicoob",
            "client": "Ada Lovelace"
        }
        response = self.client1.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authenticated_user_can_update_loan(self):
        url = f'{self.url}{self.loan1.id}/'
        data = {
            "nominal_value": "1500.00",  # Valores de exemplo para atualização
            "interest_rate": "2.00",
            "ip_address": "192.168.0.2",
            "request_date": "2022-02-15",
            "bank": "Banco Atualizado",
            "client": "Cliente Atualizado"
        }
        response = self.client1.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        updated_loan = Loan.objects.get(id=self.loan1.id)
        self.assertEqual(updated_loan.nominal_value, 1500.00)

    def test_authenticated_user_cannot_update_other_users_loan(self):
        url = f'{self.url}{self.loan2.id}/'
        data = {
            "nominal_value": "2500.00",
            "interest_rate": "3.00",
            "ip_address": "192.168.0.3",
            "request_date": "2022-02-25",
            "bank": "Banco Atualizado",
            "client": "Cliente Atualizado"
        }
        response = self.client1.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        updated_loan = Loan.objects.get(id=self.loan2.id)
        self.assertEqual(updated_loan.nominal_value, 2000.00)

    def test_unauthenticated_user_cannot_update_loan(self):
        self.client1.logout()

        url = f'{self.url}{self.loan1.id}/'
        data = {
            "nominal_value": "1500.00",
            "interest_rate": "2.00",
            "ip_address": "192.168.0.2",
            "request_date": "2022-02-15",
            "bank": "Banco Atualizado",
            "client": "Cliente Atualizado"
        }
        response = self.client1.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        loan = Loan.objects.get(id=self.loan1.id)
        self.assertEqual(loan.nominal_value, 1000.00)

    def test_authenticated_user_can_delete_loan(self):
        url = f'{self.url}{self.loan1.id}/'

        response = self.client1.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_authenticated_user_cannot_delete_others_users_loan(self):
        url = f'{self.url}{self.loan2.id}/'

        response = self.client1.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_unauthenticated_user_cannot_delete_loan(self):
        self.client1.logout()

        url = f'{self.url}{self.loan1.id}/'

        response = self.client1.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
