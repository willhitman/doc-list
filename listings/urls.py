from django.urls import path
from . import views

urlpatterns = [
    path('', views.CreateListingView.as_view(),
         name='create-listing'),
    path('<int:pk>/', views.GetUpdateDeleteListingView.as_view(),
         name='get-update-destroy'),
    path('get-all-listings/', views.GetAllListingsView.as_view(),
         name='get-all-listings'),
    path('get-by-user-id/<int:user_id>/', views.GetAllListingsByUserIdView.as_view(),
         name='get-by-user-id'),
    path('get-by-listing-type/<str:listing_type>/', views.GetListingsByListingTypeView.as_view(),
         name='get-all-by-listing-type'),


    path('languages/', views.CreateListingLanguageView.as_view(),
         name='languages'),
    path('languages/<int:pk>/', views.GetUpdateDestroyListingLanguageView.as_view(),
         name='languages-get-update-destroy'),

    path('specialization/', views.CreateListingSpecializationView.as_view(),
         name='specialization'),
    path('specialization/<int:pk>/', views.GetUpdateDestroyListingSpecializationView.as_view(),
         name='specialization-get-update-destroy'),

    path('affiliation/', views.CreateListingAffiliationView.as_view(), name='affiliation'),
    path('affiliation/<int:pk>/', views.GetUpdateDestroyListingAffiliationAndMembershipsView.as_view(),
         name='affiliation-get-update-destroy'),

    path('education/', views.CreateListingEducationalBackgroundView.as_view(),
         name='education'),
    path('education/<int:pk>/', views.GetUpdateDestroyListingEducationalBackgroundView.as_view(),
         name='education-get-update-destroy'),

    path('experience/', views.CreateListingExperienceView.as_view(),
         name='experience'),
    path('experience/<int:pk>/', views.GetUpdateDestroyListingExperienceView.as_view(),
         name='experience-get-update-destroy'),

    path('appointment/', views.CreateAppointmentsAvailabilityView.as_view(),
         name='appointment'),
    path('appointment/<int:pk>/', views.GetUpdateDestroyAppointmentsAvailabilityView.as_view(),
         name='appointment-get-update-destroy'),

    path('service/', views.CreateListingServicesView.as_view(), name='listing-service'),
    path('service/<int:pk>/', views.GetUpdateDestroyListingServicesView.as_view(),
         name='listing-service-get-update-destroy'),
    path('get-services-by-listing-id/<int:listing_id>/', views.GetListingServicesByListingIdView.as_view(),
         name='get-services-by-listing-id'),


    path('listing-profile-picture/<int:pk>/', views.ProfilePictureView.as_view(), name='listing-profile-picture'),
    path('listing-specialisation-file/<int:pk>/', views.SpecializationFileUploadView.as_view(),
         name='listing-specialisation-file'),
    path('listing-affiliation-file/<int:pk>/', views.AffiliationAndMembershipsFileUploadView.as_view(),
         name='listing-affiliation-file')


]

