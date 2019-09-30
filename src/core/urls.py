from django.urls import path, re_path
from .views import HomePageView

app_name = 'core'

urlpatterns = [
    path('', HomePageView, name='home_page'),
]