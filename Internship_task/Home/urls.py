from django.urls import path
from .import views

app_name = 'Home'

urlpatterns = [
    path('', views.Registration.as_view(), name="register"),
    path('login/', views.login, name="log"),
    path('profile/', views.profile, name="profile"),
    path('user_application/', views.user_app, name="application"),
    path('verify/', views.verify, name="verify")
]
