from django.urls import path
from rest_framework_simplejwt.views import TokenVerifyView, TokenRefreshView, TokenObtainPairView
from accounts import views

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token-obtain-pair'),
    path('token/refresh/', TokenRefreshView.as_view()),
    path('token/verify/', TokenVerifyView.as_view()),
    path('create/', views.CreateAccountView.as_view()),
    # path('service_accounts/<int:user_id>/', views.CheckServicesView.as_view()),
    ]
