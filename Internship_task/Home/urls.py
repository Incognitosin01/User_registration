from django.urls import path
from .import views

app_name = 'Home'

urlpatterns = [
    path('', views.Registration.as_view(), name="register"),
    path('login/', views.login_user, name="login"),
    path('verified_login/', views.verified_login, name="verified_login"),
    path('logout/', views.logout_user, name="logout"),
    path('profile/', views.profile, name="profile"),
    path('user_application/', views.user_app, name="application"),
    path('verify/', views.verify, name="verify"),
    path('app_submit/', views.application, name="app_submit"),
    path('otp/', views.VerifyOTP.as_view(), name="otp"),
]
