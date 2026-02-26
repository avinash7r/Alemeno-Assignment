from django.core.management.base import BaseCommand
import pandas as pd
from customers.models import Customer

class Command(BaseCommand):
    help = "Ingest customer data from Excel"

    def handle(self, *args, **kwargs):
        df = pd.read_excel("data/customer_data.xlsx")

        # normalize column names
        df.columns = (
            df.columns
            .str.strip()
            .str.lower()
            .str.replace(" ", "_")
        )

        customers = []
        for _, row in df.iterrows():
            customers.append(
                Customer(
                    id=row["customer_id"],
                    first_name=row["first_name"],
                    last_name=row["last_name"],
                    age=row["age"],
                    phone_number=str(row["phone_number"]),
                    monthly_salary=row["monthly_salary"],
                    approved_limit=row["approved_limit"],
                    current_debt=0
                )
            )

        Customer.objects.bulk_create(customers, ignore_conflicts=True)
        self.stdout.write(self.style.SUCCESS("Customers ingested"))