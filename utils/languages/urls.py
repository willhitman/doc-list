from django.urls import path
from . import views

urlpatterns = [
    path('language/create-language/', views.CreateLanguagesView.as_view(), name="create-language")
]
