from django.urls import path
# Import Views

from .import views

app_name = 'Home'

urlpatterns = [
    path('',views.user_reg, name="register"),
    path('login/', views.login, name="log"),
    path('profile/', views.profile, name="profile"),
    path('user_application/',views.user_app, name="application")
    # Add your url config below
]
