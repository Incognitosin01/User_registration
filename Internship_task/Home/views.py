from django.shortcuts import render


def login(request):
    response = "Hello, world"
    return render(request, 'html/login.html', {'var': response})
