from django.urls import path, re_path
from django.contrib.auth import views as auth_views
from .views import (
    AuthLoginView, 
    AuthLogout, 
    AuthRegister,

)

app_name = 'auth'

urlpatterns = [
    path(
        'login/',
        auth_views.LoginView.as_view(
            template_name='auth/login.html'
        ),
        name='login'),
    path(
        'register/',
        AuthRegister.as_view(
            template_name="auth/register.html"
        ),
        name='register'
    ),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
