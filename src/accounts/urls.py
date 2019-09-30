from django.urls import path, re_path
from .views import AuthHomePage

app_name = 'auth'

urlpatterns = [
    path('', AuthHomePage.as_view(), name='home'),
]