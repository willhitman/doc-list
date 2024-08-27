from django.urls import path
from . import views

urlpatterns = [
    path('languages/', views.CreateLanguageView.as_view(), name='languages'),
    path('languages/<int:pk>/', views.GetUpdateDestroyLanguageView.as_view(), name='languages-get-update-destroy'),
    path('get-all-languages/', views.GetAllLanguagesView.as_view(), name='get-all-languages'),
]
