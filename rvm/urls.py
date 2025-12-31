from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import DepositCreateView, UserSummaryView, RegisterView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', obtain_auth_token, name='login'), # DRF provides this!
    path('deposit/', DepositCreateView.as_view(), name='deposit-create'),
    path('summary/', UserSummaryView.as_view(), name='user-summary'),
]