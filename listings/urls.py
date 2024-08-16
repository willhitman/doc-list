from django.urls import path
from . import views

urlpatterns = [
    path('', views.CreateListingView.as_view(), name='create-lisitng'),
    path('<int:pk>/', views.GetUpdateDeleteListingView.as_view(), name='get-update-destroy'),
    path('get-all-listings/', views.GetAllListingsView.as_view(), name='get-all-listings'),
    path('get-by-user-id/<int:user_id>/', views.GetAllListingsByUserIdView.as_view(), name='get-by-user-id'),
    path('get-by-listing-type/<str:listing_type>/', views.GetListingsByListingTypeView.as_view(), name='get-all-by-listing-type')
]

