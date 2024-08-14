from django.urls import path

from utils.address import views

urlpatterns = [
    path('address/', views.AddressCreateView.as_view()),
    path('address/<int:pk>/', views.AddressReadUpdateDestroyView.as_view()),
]