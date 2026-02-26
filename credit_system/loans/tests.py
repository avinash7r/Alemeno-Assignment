from rest_framework.test import APITestCase
from rest_framework import status
from customers.models import Customer
from loans.models import Loan


class RegisterCustomerTest(APITestCase):

    def test_register_customer(self):
        payload = {
            "first_name": "Avi",
            "last_name": "Rajure",
            "age": 22,
            "monthly_income": 50000,
            "phone_number": "9999999999"
        }

        response = self.client.post("/api/register", payload, format="json")

        self.assertIn(
            response.status_code,
            [status.HTTP_200_OK, status.HTTP_201_CREATED]
        )
        self.assertEqual(Customer.objects.count(), 1)

        customer = Customer.objects.first()
        self.assertEqual(customer.approved_limit, 1800000)

class CreateLoanTest(APITestCase):

    def setUp(self):
        self.customer = Customer.objects.create(
            first_name="Avi",
            last_name="Rajure",
            age=22,
            phone_number="8888888888",
            monthly_salary=50000,
            approved_limit=1800000,
            current_debt=0
        )

    def test_create_loan(self):
        payload = {
            "customer_id": self.customer.id,
            "loan_amount": 300000,
            "interest_rate": 10,
            "tenure": 12
        }

        response = self.client.post("/api/create-loan", payload, format="json")

        self.assertIn(
            response.status_code,
            [status.HTTP_200_OK, status.HTTP_201_CREATED]
        )
        self.assertEqual(Loan.objects.count(), 1)
        self.assertTrue(response.data["loan_approved"])

