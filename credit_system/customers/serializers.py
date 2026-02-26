from rest_framework import serializers
from customers.models import Customer

class RegisterCustomerSerializer(serializers.ModelSerializer):
    monthly_income = serializers.IntegerField(write_only=True)
    name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Customer
        fields = [
            "id",
            "first_name",
            "last_name",
            "age",
            "phone_number",
            "monthly_income",
            "approved_limit",
            "name"
        ]
        read_only_fields = ["id", "approved_limit", "name"]

    def get_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"

    def create(self, validated_data):
        monthly_income = validated_data.pop("monthly_income")

        approved_limit = round((36 * monthly_income) / 100000) * 100000

        return Customer.objects.create(
            monthly_salary=monthly_income,
            approved_limit=approved_limit,
            current_debt=0,
            **validated_data
        )
