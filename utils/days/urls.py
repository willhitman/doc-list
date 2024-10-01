from rest_framework.urls import path

from . import views

urlpatterns = [
    path('day/', views.CreateDayView.as_view(), name='create-day'),
    path('day/<int:pk>/', views.GetUpdateDestroyView.as_view(), name='get-update-destroy-day-view')
]
