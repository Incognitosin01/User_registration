from django.http.response import JsonResponse
from django.shortcuts import render
from django.views import View
from django.shortcuts import redirect
from django.conf import settings
from django.urls import reverse
from django.contrib import messages
import hashlib
import os
import json
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .models import (CustomUser, Application)
from django.core.mail import send_mail
from django.contrib.auth import (logout, login)
from typing import Any
from twilio.rest import Client
from twilio.base.exceptions import TwilioException
import requests
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt


class Registration(View):
    def __init__(self):
        super(Registration, self).__init__()
        self.hash_util = os.environ.get('verification_hash') or 'random_string'

    def get(self, request):
        return render(request, 'html/Registration_Page.html')

    def post(self, request):
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        phone_number = request.POST['phone']
        password = request.POST['password']
        email = request.POST['email']

        user = CustomUser.objects.create_user(username=email, first_name=first_name,last_name=last_name, password=password, email=email,contact=phone_number)
        
        user.is_active = False
        user.save()

        hash_object = hashlib.md5((email + self.hash_util).encode())
        hashed_string = hash_object.hexdigest()

        subject, from_email, to = 'Verification', settings.EMAIL_HOST_USER, user.email
        url = f"{request.scheme}://{request.get_host()}{reverse('Home:verify')}?key={hashed_string}&email={user.email}"
        html_content = render_to_string('html/verification_template.html', {'url': url})
        text_content = strip_tags(html_content)
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        messages.success(request, "We've sent you a verification mail. \
        Follow the instructions in mail to complete your registration")
        return redirect(reverse("Home:register"))


def verify(request):
    hash_util = os.environ.get('verification_hash') or 'random_string'
    email = request.GET['email']
    key = request.GET['key']
    if hashlib.md5((email + hash_util).encode()).hexdigest() == key:
        messages.success(request, 'Verification successful', 'success')
        user = CustomUser.objects.get(email=email)
        user.is_active = True
        user.save()
        return redirect(reverse('Home:login'))
    messages.error(request, 'Verification failed', 'error')
    return redirect('/')

def login_user(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect(reverse("Home:profile"))
        else:
            return render(request, 'html/login.html')
    
    phone_number = request.POST['contact']
    password = request.POST['password']

    # contact=phone_number needs a full phone number with country code
    user = CustomUser.objects.filter(contact = phone_number)
    if not user:
        messages.error(request, "You've not registered yet")
        return redirect(reverse('Home:register'))
    else:
        authenticated = user.first().check_password(password)
        if authenticated:
            login(request, user.first())
            return redirect(reverse("Home:application"))
    messages.error(request, "Invalid credentials")
    return redirect(reverse("Home:login"))


def logout_user(request):
    if request.user.is_anonymous:
        return redirect(reverse('Home:login'))
    logout(request)
    messages.success(request, 'Successfully logged out')
    return redirect(reverse('Home:login'))

def profile(request):
    if request.user.is_anonymous:
        messages.error(request, 'You are not logged in')
        return redirect(reverse('Home:login'))
    app = Application.objects.filter(F_key=request.user)
    
    if not app:
        messages.error(request,'Please fill application form first')
        return redirect(reverse('Home:application'))
    
    app = Application.objects.values('address','resume','Marksheet','aadhar').get(F_key=request.user)
    return render(request, 'html/index.html',{'addr':app['address'],'resume':app['resume'],'marks':app['Marksheet'],'aadhar':app['aadhar']})

def user_app(request):
    if request.user.is_anonymous:
        messages.error(request, 'You are not logged in')
        return redirect(reverse('Home:login'))
    return render(request, 'html/application.html')

def application(request):
    if request.method=="POST":
        email= request.POST['email']
        address = request.POST['address']
        resume = request.POST['resume']
        adhaar = request.POST['adhaar']
        marksheet = request.POST['marksheet']
        user=CustomUser.objects.get(email=request.user.email)
        try:
            app = Application.objects.get(F_key=request.user)
            app=Application.objects.get(F_key=request.user)
            app.address=address
            app.aadhar=adhaar
            app.Marksheet=marksheet
            app.resume=resume
            app.save()
        except Application.DoesNotExist:
            application = Application(F_key=user,address=address, aadhar=adhaar, resume=resume, Marksheet=marksheet)
            application.save()
    
        
        send_mail(
            "Application",
            "Your Application has submitted successfully",
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False,
        )
    return render(request,'html/index.html',{'addr':address,'resume':resume,'marks':marksheet,'aadhar':adhaar})


@method_decorator(csrf_exempt, name='dispatch')
class VerifyOTP(View):
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.otp_url = 'https://api.generateotp.com/'
        try:
            self.twilio_client = Client()
            self.sender = os.getenv('TWILIO_NUMBER')
        except TwilioException:
            from .twilio_conf import TWILIO_NUMBER, AUTH_TOKEN, ACCOUNT_SID
            self.twilio_client = Client(ACCOUNT_SID, AUTH_TOKEN)
            self.sender = TWILIO_NUMBER

    def get(self, request):
        phone_number = request.GET['phone']
        country_code = request.GET['country_code']
        
        country_code_size = len(country_code)

        user = CustomUser.objects.filter(contact=f"+{phone_number}")
        if not user:
            return JsonResponse({'status': 302,'message': 'Number you\'re trying to log in is not registered'})
        
        req = requests.post(f"{self.otp_url}/generate", data={'initiator_id': phone_number[country_code_size:]})

        if req.status_code != 201:
            return JsonResponse({'status': 500, 'message': 'Error occurred, please retry'})
        
        otp = str(req.json()['code'])
        message = f"Your one time password for login is {otp}"

        self.twilio_client.messages.create(to=f"+{phone_number}", from_=self.sender, body=message)
        return JsonResponse({'status': 201, 'message': 'OTP sent successfully'})

    def post(self, request):
        p = json.loads(request.body)
        otp = p['otp_code']
        phone_number = p['phone']
        req = requests.post(f"{self.otp_url}/validate/{otp}/{phone_number}")
        return JsonResponse(req.json())
