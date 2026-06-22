from django.urls import path
from .views import CountriesAPIView

urlpatterns = [
    path('countries/', view=CountriesAPIView.as_view(), name='countries')
]