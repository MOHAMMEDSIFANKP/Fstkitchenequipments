from django.shortcuts import render
from django.views.generic import *
from dashboard.models import BgImages
# Create your views here.

class Home(ListView):
    template_name = 'user/home.html'
    context_object_name = 'data_list'

    def get_queryset(self):
        bg_images = BgImages.objects.all()
        return {'bg_images': bg_images}
   

class Category(TemplateView):
    template_name = 'user/category_page.html'

class sifan(TemplateView):
    template_name = 'user/sifan.html'