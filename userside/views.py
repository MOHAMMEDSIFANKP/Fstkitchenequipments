from django.shortcuts import render
from django.views.generic import *
# Create your views here.

class Home(TemplateView):
    template_name = 'user/home.html'

class Category(TemplateView):
    template_name = 'user/category_page.html'