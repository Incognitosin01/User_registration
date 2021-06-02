from django.shortcuts import render


def user_reg(request):
    return render(request, 'html/Registration_Page.html')

def login(request):
    response = "Hello, world"
    return render(request, 'html/login.html', {'var': response})

def profile(request):
    return render(request,'HTML/index.html')

def user_app(request):
    return render(request,'html/application.html')
