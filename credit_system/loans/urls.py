from django.urls import path
from loans.views import CheckEligibilityView

urlpatterns = [
    path("check-eligibility", CheckEligibilityView.as_view()),
]