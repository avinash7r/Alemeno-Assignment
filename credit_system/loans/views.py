from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from customers.models import Customer
from loans.models import Loan
from loans.serializers import CheckEligibilitySerializer, CreateLoanSerializer, LoanDetailSerializer, LoanListSerializer
from loans.services import check_loan_eligibility, calculate_emi, check_loan_eligibility

from dateutil.relativedelta import relativedelta
from datetime import date

class CheckEligibilityView(APIView):

    def post(self, request):
        serializer = CheckEligibilitySerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data

        try:
            customer = Customer.objects.get(id=data["customer_id"])
        except Customer.DoesNotExist:
            return Response(
                {"error": "Customer not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        result = check_loan_eligibility(
            customer=customer,
            loan_amount=data["loan_amount"],
            interest_rate=data["interest_rate"],
            tenure=data["tenure"]
        )

        return Response(
            {
                "customer_id": customer.id,
                "approval": result["approved"],
                "interest_rate": data["interest_rate"],
                "corrected_interest_rate": result["corrected_interest_rate"],
                "tenure": data["tenure"],
                "monthly_installment": result["monthly_installment"]
            },
            status=status.HTTP_200_OK
        )

class CreateLoanView(APIView):

    def post(self, request):
        serializer = CreateLoanSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data

        try:
            customer = Customer.objects.get(id=data["customer_id"])
        except Customer.DoesNotExist:
            return Response(
                {"message": "Customer not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        result = check_loan_eligibility(
            customer,
            data["loan_amount"],
            data["interest_rate"],
            data["tenure"]
        )

        if not result["approved"]:
            return Response(
                {
                    "loan_id": None,
                    "customer_id": customer.id,
                    "loan_approved": False,
                    "message": "Loan not approved",
                    "monthly_installment": result["monthly_installment"]
                },
                status=status.HTTP_200_OK
            )

        # APPROVED → create loan
        start_date = date.today()
        end_date = start_date + relativedelta(months=data["tenure"])

        loan = Loan.objects.create(
            customer=customer,
            loan_amount=data["loan_amount"],
            interest_rate=result["corrected_interest_rate"],
            tenure=data["tenure"],
            monthly_installment=result["monthly_installment"],
            emis_paid_on_time=0,
            start_date=start_date,
            end_date=end_date,
            is_active=True
        )

        # update customer debt
        customer.current_debt += data["loan_amount"]
        customer.save()

        return Response(
            {
                "loan_id": loan.id,
                "customer_id": customer.id,
                "loan_approved": True,
                "message": "Loan approved",
                "monthly_installment": loan.monthly_installment
            },
            status=status.HTTP_201_CREATED
        )

class ViewLoanView(APIView):

    def get(self, request, loan_id):
        try:
            loan = Loan.objects.select_related("customer").get(id=loan_id)
        except Loan.DoesNotExist:
            return Response(
                {"error": "Loan not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = LoanDetailSerializer(loan)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ViewCustomerLoansView(APIView):

    def get(self, request, customer_id):
        try:
            customer = Customer.objects.get(id=customer_id)
        except Customer.DoesNotExist:
            return Response(
                {"error": "Customer not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        loans = customer.loans.filter(is_active=True)
        serializer = LoanListSerializer(loans, many=True)
    
        return Response(serializer.data, status=status.HTTP_200_OK)
    



