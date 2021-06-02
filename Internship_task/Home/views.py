from django.shortcuts import render


def user_reg(request):
    return render(request, 'html/Registration_Page.html')

def login(request):
    return render(request, 'html/login.html')

def profile(request):
    return render(request,'html/index.html')

def user_app(request):
    return render(request,'html/application.html')
