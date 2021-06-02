from django.urls import path
# Import Views
from .views import login

urlpatterns = [
    path('login/', login)
    # Add your url config below
]
