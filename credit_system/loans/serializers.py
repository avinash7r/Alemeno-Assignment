from rest_framework import serializers

from customers.models import Customer
from loans.models import Loan

class CheckEligibilitySerializer(serializers.Serializer):
    customer_id = serializers.IntegerField()
    loan_amount = serializers.FloatField()
    interest_rate = serializers.FloatField()
    tenure = serializers.IntegerField()

class CreateLoanSerializer(serializers.Serializer):
    customer_id = serializers.IntegerField()
    loan_amount = serializers.FloatField()
    interest_rate = serializers.FloatField()
    tenure = serializers.IntegerField()

class CustomerMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ["id", "first_name", "last_name", "phone_number", "age"]

class LoanDetailSerializer(serializers.ModelSerializer):
    customer = CustomerMiniSerializer()

    class Meta:
        model = Loan
        fields = [
            "id",
            "customer",
            "loan_amount",
            "interest_rate",
            "monthly_installment",
            "tenure",
        ]
