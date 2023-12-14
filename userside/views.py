from django.shortcuts import render,redirect
from django.views.generic import *
from dashboard.models import *
from django.http import JsonResponse
from django.db.models import Q
# Create your views here.

class Home(TemplateView):
    template_name = 'user/home/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["bg_images"] = BgImages.objects.all()
        context["category_data"] = Categories.objects.all().order_by('name')
        context["products_data"] = Products.objects.all()[:8]
        return context

    def get(self, request, *args, **kwargs):
        if request.GET.get('methods') == 'search':
            query = request.GET.get('query', '').strip()
            instance_data = Products.objects.filter(Q(name__icontains=query) | Q(category__name__icontains=query))[:8]
            return render(request, 'user/home/search_data.html', {'products_data': instance_data})

        if request.GET.get('methods') == 'category':
            id = request.GET.get('id', '').strip()
            if id == 'all':
                instance_data = Products.objects.all()[:8]
            else:
                try:
                    instance_data = Products.objects.filter(category__id=id)
                except:
                    return render(request, 'user/home/search_data.html', {'products_data': instance_data})

            return render(request, 'user/home/search_data.html', {'products_data': instance_data})
        
        return super().get(request, *args, **kwargs)
    
class Category_List(ListView):
    template_name = 'user/category/category_list.html'
    context_object_name = 'data_list'

    def get_queryset(self):
        category_data = Categories.objects.all().order_by('name')
        return {'category_data' : category_data}
    
class Product_List(ListView):
    template_name = 'user/products_list.html'
    context_object_name = 'data_list'

    def get_queryset(self):
        category_id = self.kwargs.get('pk', None)
        category_data = Categories.objects.all().order_by('name')
        if category_id:
            try:
                products_data = Products.objects.filter(category_id=category_id)
            except Products.DoesNotExist:
                return redirect('Category_List')
            return {'products_data':products_data,'category_data':category_data}
        else:
            return redirect('Category_List')
        
    def get(self, request, *args, **kwargs):
        if request.GET.get('methods') == 'search':
            query = request.GET.get('query', '').strip()
            instance_data = Products.objects.filter(Q(name__icontains=query) | Q(category__name__icontains=query))[:8]
            return render(request, 'user/home/search_data.html', {'products_data': instance_data})

        if request.GET.get('methods') == 'category':
            id = request.GET.get('id', '').strip()
            if id == 'all':
                instance_data = Products.objects.all()[:8]
            else:
                try:
                    instance_data = Products.objects.filter(category__id=id)
                except:
                    return render(request, 'user/home/search_data.html', {'products_data': instance_data})

            return render(request, 'user/home/search_data.html', {'products_data': instance_data})
        
        return super().get(request, *args, **kwargs)
    