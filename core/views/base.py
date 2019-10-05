# import json
import logging

#from django.shortcuts import render
from django.http.response import HttpResponse
from django.views.generic import ListView, DetailView
from django.views.generic.base import View, TemplateView

logger = logging.getLogger(__name__)

class Dashboard(TemplateView):
    template_name = 'core/index.html'

class NotFoundView(TemplateView):
    template_name = '404.html'