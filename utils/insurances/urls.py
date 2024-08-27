from django.urls import path
from . import views

urlpatterns=[
    path('insurance/', views.CreateInsuranceView.as_view(), name='insurance'),
    path('insurance/<int:pk>/', views.GetUpdateDestroyInsuranceView.as_view(), name='insurance-get-update-destroy'),
    path('get-all-insurance/', views.GetAllInsurancesView.as_view(), name='get-all-insurance'),
]