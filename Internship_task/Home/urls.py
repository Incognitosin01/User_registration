from os import name, stat
from django.urls import path
from .import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'Home'

urlpatterns = [
    path('registration/', views.Registration.as_view(), name="register"),
    path('', views.login_user, name="login"),
    path('logout/', views.logout_user, name="logout"),
    path('profile/', views.profile, name="profile"),
    path('user_application/', views.user_app, name="application"),
    path('verify/', views.verify, name="verify"),
    path('app_submit/', views.application, name="app_submit"),
    path('otp/', views.VerifyOTP.as_view(), name="otp"),
]


