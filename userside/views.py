from django.shortcuts import render,redirect
from django.views.generic import *
from dashboard.models import *
# Create your views here.

class Home(ListView):
    template_name = 'user/home.html'
    context_object_name = 'data_list'

    def get_queryset(self):
        bg_images = BgImages.objects.all()
        category_data = Categories.objects.all().order_by('name')
        products_data = Products.objects.all()[:8]
        return {'bg_images': bg_images,'category_data' : category_data,'products_data':products_data}
   
class Category_List(ListView):
    template_name = 'user/category_list.html'
    context_object_name = 'data_list'

    def get_queryset(self):
        category_data = Categories.objects.all().order_by('name')
        return {'category_data' : category_data}
    
class Product_List(ListView):
    template_name = 'user/products_list.html'
    context_object_name = 'data_list'

    def get_queryset(self):
        category_id = self.kwargs.get('pk', None)
        if category_id:
            try:
                products_data = Products.objects.filter(category_id=category_id)
            except Products.DoesNotExist:
                return redirect('Category_List')
            return {'products_data':products_data}
        else:
            return{'products_data': Products.objects.all()}

    