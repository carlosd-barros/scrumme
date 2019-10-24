from django.urls import path, re_path
from django.contrib.auth import views as auth_views
from .views import AuthRegisterView

app_name = 'accounts'

urlpatterns = [
    path('register/', AuthRegisterView.as_view(), name='register'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
