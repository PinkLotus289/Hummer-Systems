
from django.urls import path
from .views import (
    SendCodeView,
    VerifyCodeView,
    ProfileView,
    UseInviteView
)

# users/urls.py
urlpatterns = [
    path('phone/', SendCodeView.as_view(), name='auth-phone'),
    path('verify/', VerifyCodeView.as_view(), name='auth-verify'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/use_invite/', UseInviteView.as_view(), name='use-invite'),
]


