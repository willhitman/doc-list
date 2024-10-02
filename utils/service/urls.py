from django.urls import path
from . import views

urlpatterns = [
    path('service/', views.CreateServiceView.as_view(), name='service'),
    path('service/<int:pk>/', views.GetUpdateDestroyServicesView.as_view(),
         name='service-get-update-destroy'),
    path('get-all-service/', views.GetAllServicesView.as_view(),
         name='get-all-services')
]