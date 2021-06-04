from django.shortcuts import render
from django.views import View
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.conf import settings
from django.urls import reverse
from django.contrib import messages
import hashlib
import os
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .models import CustomUser,Application
from django.core.mail import send_mail
from django.contrib.auth import (authenticate, login)


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
        return redirect("/")


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
        return render(request, 'html/login.html')
    
    user = authenticate(request, username=request.POST['contact'], password=request.POST['password'])
    if user is not None:
        login(request, user)
        return redirect(reverse('Home:application'))
    messages.error(request, "Invalid credentials")
    return redirect(reverse("Home:login"))


def profile(request):
    return render(request, 'html/index.html')

def user_app(request):
    return render(request, 'html/application.html')

def application(request):
    if request.method=="POST":
        email= request.POST['email']
        address = request.POST['address']
        resume = request.POST['resume']
        adhaar = request.POST['adhaar']
        marksheet = request.POST['marksheet']
        user=CustomUser.objects.get(email=email)
        application = Application(F_key=user,address=address, aadhar=adhaar, resume=resume, Marksheet=marksheet)
        application.save()
        send_mail(
            "Application",
            "Your Application has submitted successfully",
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False,
        )
    return redirect('/')
