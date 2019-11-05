from django.urls import path, re_path
from django.urls.base import reverse_lazy
from django.contrib.auth import views as auth_views
from .views import AuthRegisterView

app_name = 'accounts'

urlpatterns = [
    path('register/', AuthRegisterView.as_view(), name='register'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path(
        'login/',
        auth_views.LoginView.as_view(
            template_name='auth/login.html'
        ),
        name='login'
    ),
    path(
        'password-reset',
        auth_views.PasswordResetView.as_view(
            template_name='auth/password_reset.html',
            success_url=reverse_lazy(
                'accounts:password_reset'
            ),
        ),
        name='password_reset'
    ),
    path(
        'password-reset/done',
        auth_views.PasswordResetView.as_view(
            template_name='auth/password_reset_done.html'
        ),
        name='password_reset_done'
    ),
    path(
        'password-reset-confirm/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='auth/password_reset_confirm.html'
        ),
        name='password_reset_confirm'
    ),
    path('password-reset-complete/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='auth/password_reset_complete.html'
        ),
        name='password_reset_complete'
    ),
]