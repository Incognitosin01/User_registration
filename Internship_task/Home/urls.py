from django.urls import path
# Import Views
from .views import login

app_name = 'Home'

urlpatterns = [
    path('login/', login),
    # Add your url config below
]
