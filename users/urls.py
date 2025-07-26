from django.urls import path, include
from .views import (
    Register,
    SendOTPView,
    VerifyOTPView,
    ProfileView,
    ActivateInviteView, ActivateInviteWebView,
)


app_name = 'users'

urlpatterns = [

    path('', include("django.contrib.auth.urls")),
    path('register/', Register.as_view(), name='register'),
    path('auth/phone/', SendOTPView.as_view(), name='send-otp'),
    path('auth/verify/', VerifyOTPView.as_view(), name='verify-otp'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/activate/', ActivateInviteView.as_view(), name='activate-invite'),
    path('profile/activate-web/', ActivateInviteWebView.as_view(), name='activate-invite-web'),

]
