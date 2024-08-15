from django.urls import path
from . import views
urlpatterns = [
    path('', views.CreateListingView.as_view(), name='create-lisitng'),
]