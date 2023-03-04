from django.http import HttpResponse
from django.shortcuts import render
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.auth.models import auth

from UserAccounts.models import *

import random




# global support functions

def sendOTPEmail(rd):

    check_otp = random.randint(10000, 99999)
    subject = f"Welcome to ByteCodes {rd['first_name']}"
    msg = f"OTP :: {check_otp}"
    html_message = render_to_string('temp/otp_email.html', {"check_otp": check_otp, "sender": settings.EMAIL_HOST_USER, "receiver": rd['email']})
    # print("html_message :: ", html_message)
    
    res = send_mail(subject, msg, settings.DEFAULT_FROM_EMAIL, [rd['email'], "siddhirajk77gmail.com"], html_message=html_message, fail_silently=False)

    print("res :: ", res)
    if res == 1:
        otp.objects.filter(email=rd['email']).delete()
        new_otp = otp.objects.create(email=rd['email'], otp=check_otp)

        return True
    else:
        return False


# Create your views here.


def Register(request):

    if request.method == "POST":

        rd = request.POST
        se = sendOTPEmail(rd)
        if not se:
            return HttpResponse("Something went wrong!")
        
        new_user = CustomUser.objects.create_user(username=rd['username'], password=rd['password'], email=rd['email'],
                                                  first_name=rd['first_name'], last_name=rd['last_name'])
        new_user.save()

        data = {
            "email": rd['email'],
            "message": ""
        }

        return render(request, 'temp/verify_otp.html', data)

    return render(request, 'temp/register.html')


def VerifyOTP(request):

    rd = request.POST
    print("rd :: ", rd)
    
    if rd['email'] in ["", None]:
        return HttpResponse("Unauthorized!")

    otp_obj = otp.objects.filter(email=rd['email'], otp=rd['otp']).first()

    if otp_obj is not None:
        otp_obj.delete()

        return HttpResponse("Email Verified Successfully!!!")
    
    data = {
        "email": rd['email'],
        "message": "Invalid OTP entered!"
    }

    return render(request, 'temp/verify_otp.html', data)



def Login(request):

    if request.method == "POST":
        rd = request.POST
        print("rd :: ", rd)

        user = auth.authenticate(email=rd['email'], password=rd['password'])
        
        if user is not None:
            auth.login(request, user)

            return HttpResponse(f"<h1>Login Successful {user.first_name} !</h1>")


    return render(request, 'temp/login.html')


def Index(request):
    return render(request, 'main/index.html')


def event_detials(request):
    return render(request, 'events/event_details.html')

def user_dashboard(request):
    return render(request, 'user/dashboard.html')

def user_profile(request):
    return render(request, 'user/profile.html')

def org_dashboard(request):
    return render(request, 'org/dashboard.html')

def org_profile(request):
    return render(request, 'org/profile.html')