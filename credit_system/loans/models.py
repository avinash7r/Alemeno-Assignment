from django.db import models
from customers.models import Customer

class Loan(models.Model):
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name="loans"
    )

    loan_amount = models.FloatField()
    interest_rate = models.FloatField()
    tenure = models.IntegerField()

    monthly_installment = models.FloatField()
    emis_paid_on_time = models.IntegerField(default=0)

    start_date = models.DateField()
    end_date = models.DateField()

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Loan {self.id} - Customer {self.customer_id}"