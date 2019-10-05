from django.views.generic.base import RedirectView
from django.urls import path, re_path
from .views.base import (
    Dashboard,
    NotFoundView
)

app_name='core'

urlpatterns = [
    path('', Dashboard.as_view(), name='dashboard'),
    path('404/', NotFoundView.as_view(), name='404')
]