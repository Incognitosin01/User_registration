from django.shortcuts import render
from django.views import View
from django.contrib.auth.models import User
from .models import Application
from django.core.mail import send_mail
from django.shortcuts import redirect
import hashlib


class Registration(View):
    def get(self, request):
        return render(request, 'html/Registration_Page.html')

    def post(self, request):
        first_name = request.post['first_name']
        last_name = request.post['last_name']
        phone_number = request.post['phone_number']
        password = request.post['password']
        email = request.post['email']

        user = User.objects.create_user(first_name=first_name, last_name=last_name, 
                                        password=password, email=email)
        user.save()

        hash_object = hashlib.md5(email.encode())
        hashed_string = hash_object.hexdigest()
        
        send_mail('[important] Email verification',f'Click on the below link to complete your registration
        {hashed_string}','from@example.com', [user.email],  fail_silently=False,)

        return redirect("/")

def login(request):
    return render(request, 'html/login.html')

def profile(request):
    return render(request,'html/index.html')

def user_app(request):
    return render(request,'html/application.html')
