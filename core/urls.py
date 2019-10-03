from django.urls import path, re_path
from .views import Dashboard

app_name = 'core'

urlpatterns = [
    path('', Dashboard.as_view(), name='dashboard'),
]