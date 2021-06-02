from django.http import HttpResponse


def login(request):
    response = "Hello, world"
    return HttpResponse(response)
