import json
import logging

#from django.shortcuts import render
from django.http.response import HttpResponse
from django.views.generic import ListView, DetailView
from django.views.generic.base import View, TemplateView

logger = logging.getLogger(__name__)

def HomePageView(request):
    html = """
    <body>
        <h1>Hello world<h1/>
    <body>
    """

    return HttpResponse(html)