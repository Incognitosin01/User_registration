from django.urls import path
# Import Views

from .import views

app_name = 'Home'

urlpatterns = [
    path('',views.user_reg),
    path('login/', views.login),
    path('profile/', views.profile),
    path('user_application/',views.user_app)
    # Add your url config below
]
