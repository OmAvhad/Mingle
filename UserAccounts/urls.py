from django.urls import path
from UserAccounts.views import *

app_name = 'UserAccounts'
urlpatterns = [
    path('', Index, name="index"),
    path('register', Register, name="register"),
    path('verify', VerifyOTP, name="verify-otp"),
    path('login', Login, name="login"),
    path('logout', Logout, name="logout"),
    path('index', Index, name="index"),
    path('event', event_detials, name="event_details"),
    
    # user
    path('dashboard', user_dashboard, name="user_dash"),
    path('profile', user_profile, name="user_profile"),
    path('profile/details', ProfileDetails, name="profile-details"),
    
    # org
    path('org/register', Register, name="org_register"),
    path('org/dashboard', org_dashboard, name="org_dash"),
    path('org/profile', org_profile, name="org_profile"),
]

