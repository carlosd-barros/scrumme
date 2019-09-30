import json
from django.shortcuts import render
from django.views.generic import ListView, TemplateView

from django.http.response import HttpResponse
from django.views.generic.base import View


class AuthHomePage(TemplateView):
    template_name = 'accounts/index.html'