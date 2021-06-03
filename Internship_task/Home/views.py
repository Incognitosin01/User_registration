from django.shortcuts import render
from django.views import View
from django.contrib.auth.models import User
from .models import Application
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.conf import settings
from django.urls import reverse
from django.contrib import messages
import hashlib
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

class Registration(View):
    def get(self, request):
        return render(request, 'html/Registration_Page.html')

    def post(self, request):
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        phone_number = request.POST['phone']
        password = request.POST['password']
        email = request.POST['email']

        user = User.objects.create_user(username=phone_number, first_name=first_name, last_name=last_name, 
                                        password=password, email=email)
        user.is_active = False
        user.save()

        hash_object = hashlib.md5(email.encode())
        hashed_string = hash_object.hexdigest()

        subject, from_email, to = 'Verification', settings.EMAIL_HOST_USER, user.email
        html_content = render_to_string('html/verification_template.html', {'key': hashed_string, 'email': user.email})
        text_content = strip_tags(html_content)
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        return redirect("/")

def verify(request):
    email = request.GET['email']
    key = request.GET['key']
    if hashlib.md5(email.encode()).hexdigest() == key:
        messages.success(request, 'Verification successfull', 'success')
        user = User.objects.get(email=email)
        user.is_active = True 
        user.save()
        return redirect(reverse('Home:log'))
    messages.error(request, 'Verification failed', 'error')
    return redirect('/')

def test(request):
    hashed_string = "bkdshhfsbksb"
    email = "msdfv@gmail.com"
    return render(request, 'html/verification_template.html', {'key': hashed_string, 'email': email})

def login(request):
    return render(request, 'html/login.html')

def profile(request):
    return render(request,'html/index.html')

def user_app(request):
    return render(request,'html/application.html')
