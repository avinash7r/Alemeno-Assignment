from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = "Reset PostgreSQL sequences for customers and loans"

    def handle(self, *args, **kwargs):
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT setval(
                    pg_get_serial_sequence('customers_customer', 'id'),
                    COALESCE(MAX(id), 1)
                ) FROM customers_customer;
            """)

            cursor.execute("""
                SELECT setval(
                    pg_get_serial_sequence('loans_loan', 'id'),
                    COALESCE(MAX(id), 1)
                ) FROM loans_loan;
            """)

        self.stdout.write(self.style.SUCCESS("Postgres sequences reset"))