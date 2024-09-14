from rest_framework.urls import path

from . import views

urlpatterns = [
    path('days/', views.CreateDayView.as_view(), name='create-day'),
]
