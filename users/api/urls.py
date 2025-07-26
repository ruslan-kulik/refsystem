from users.views import (
    SendOTPView,
    VerifyOTPView,
    ProfileView,
    ActivateInviteView,
)
from django.urls import path, include

app_name = 'users_api'

urlpatterns = [
    path('auth/phone/', SendOTPView.as_view(), name='send-otp'),
    path('auth/verify/', VerifyOTPView.as_view(), name='verify-otp'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/activate/', ActivateInviteView.as_view(), name='activate-invite'),
]
