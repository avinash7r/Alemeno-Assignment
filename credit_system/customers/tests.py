from rest_framework.test import APITestCase
from rest_framework import status
from customers.models import Customer

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

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Customer.objects.count(), 1)

        customer = Customer.objects.first()
        self.assertEqual(customer.approved_limit, 1800000)