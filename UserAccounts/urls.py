from django.urls import path
from UserAccounts.views import *

app_name = 'UserAccounts'
urlpatterns = [
    path('', Index, name="index"),
    path('register', Register, name="register"),
    path('verify', VerifyOTP, name="verify-otp"),
    path('login', Login, name="login"),
]

