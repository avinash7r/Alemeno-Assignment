from django.core.management.base import BaseCommand
import pandas as pd
from loans.models import Loan
from customers.models import Customer

class Command(BaseCommand):
    help = "Ingest loan data from Excel"

    def handle(self, *args, **kwargs):
        df = pd.read_excel("/home/avi/vsCode/Alemeno/data/loan_data.xlsx")

        df.columns = (
            df.columns
            .str.strip()
            .str.lower()
            .str.replace(" ", "_")
        )

        loans = []

        for _, row in df.iterrows():
            try:
                customer = Customer.objects.get(id=row["customer_id"])
            except Customer.DoesNotExist:
                continue

            loans.append(
                Loan(
                    id=row["loan_id"],
                    customer=customer,
                    loan_amount=row["loan_amount"],
                    tenure=row["tenure"],
                    interest_rate=row["interest_rate"],
                    monthly_installment=row["monthly_payment"],
                    emis_paid_on_time=row["emis_paid_on_time"],
                    start_date=row["date_of_approval"],
                    end_date=row["end_date"],
                    is_active=True
                )
            )

        Loan.objects.bulk_create(loans, ignore_conflicts=True)
        self.stdout.write(self.style.SUCCESS("Loans ingested"))