from django.urls import path

from . import views

urlpatterns = [
    path('insurance/get-all-insurances/', views.InsuranceGetAll.as_view())
]
