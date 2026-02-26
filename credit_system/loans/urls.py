from django.urls import path
from loans.views import CheckEligibilityView, CreateLoanView

urlpatterns = [
    path("check-eligibility", CheckEligibilityView.as_view()),
        path("create-loan", CreateLoanView.as_view()),

]