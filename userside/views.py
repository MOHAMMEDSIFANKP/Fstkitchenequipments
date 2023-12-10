from django.shortcuts import render
from django.views.generic import *
from dashboard.models import *
# Create your views here.

class Home(ListView):
    template_name = 'user/home.html'
    context_object_name = 'data_list'

    def get_queryset(self):
        bg_images = BgImages.objects.all()
        category_data = Categories.objects.all()
        return {'bg_images': bg_images,'category_data' : category_data}
   
class Category_User(TemplateView):
    template_name = 'user/category_page.html'

class sifan(TemplateView):
    template_name = 'user/sifan.html'