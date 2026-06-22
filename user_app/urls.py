from rest_framework_simplejwt.views import TokenRefreshView
from django.urls import path
from .views import *

urlpatterns = [
    path('register/', view=RegistrationAPIView.as_view(), name='registration'),
    path('login/', view=LoginAPIView.as_view(), name='login'),
    path('verify-email/', view=VerifyEmailAPIView.as_view(), name='verify_email'),
    path('refresh/', view=TokenRefreshView.as_view(), name='refresh'),
    path('me/', view=MeAPIView.as_view(), name='me'),
]