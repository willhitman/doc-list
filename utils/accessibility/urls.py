from django.urls import path
from . import views

urlpatterns = [
    path('accessibility/', views.CreateAccessibilityView.as_view(), name='accessibility'),
    path('accessibility/<int:pk>/', views.GetUpdateDestroyAccessibilityView.as_view(),
         name='accessibility-get-update-destroy'),
]
