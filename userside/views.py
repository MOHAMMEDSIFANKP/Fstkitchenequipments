from django.shortcuts import render,redirect
from django.views.generic import *
from dashboard.models import *
from django.http import JsonResponse
from django.db.models import Q
from .foms import *
# Create your views here.

class Home(TemplateView):
    template_name = 'user/home/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["bg_images"] = BgImages.objects.all()
        context["category_data"] = Categories.objects.all().order_by('name')
        context["products_data"] = Products.objects.all()[:8]
        context["clients_data"] = Clients.objects.all()
        return context

    def get(self, request, *args, **kwargs):
        query = request.GET.get('query', '').strip()
        category_id = request.GET.get('category_id', '').strip()

        if request.GET.get('methods') == 'search':
            if category_id and category_id != 'all':
                instance_data = Products.objects.filter(category_id=category_id, name__icontains=query) | Products.objects.filter(category_id=category_id, category__name__icontains=query)[:8]
            else:
                instance_data = Products.objects.filter(name__icontains=query) | Products.objects.filter(category__name__icontains=query)[:8]
            return render(request, 'user/home/search_data.html', {'products_data': instance_data, 'category_id': category_id})

        if request.GET.get('methods') == 'category':
            instance_data = Products.objects.all() if category_id == 'all' else Products.objects.filter(category__id=category_id)[:8]
            return render(request, 'user/home/search_data.html', {'products_data': instance_data, 'category_id': category_id})

        return super().get(request, *args, **kwargs)

    
class Category_List(ListView):
    template_name = 'user/category/category_list.html'
    context_object_name = 'data_list'

    def get_queryset(self):
        category_data = Categories.objects.all().order_by('name')
        return {'category_data' : category_data}
    
class Product_List(ListView):
    template_name = 'user/products/products_list.html'
    context_object_name = 'data_list'

    def get_queryset(self):
        category_id = self.kwargs.get('pk')
        try:
            category_data = Categories.objects.all().order_by('name')
            products_data = Products.objects.filter(category_id=category_id) if category_id else Products.objects.all()
        except:
            return redirect(Category_List)
        return {'products_data': products_data, 'category_data': category_data, 'category_id': category_id}

    def get(self, request, *args, **kwargs):
        query = request.GET.get('query', '').strip()
        category_id = request.GET.get('category_id', '').strip()

        if request.GET.get('methods') == 'search':
            if category_id and category_id != 'all':
                instance_data = Products.objects.filter(category_id=category_id, name__icontains=query) | Products.objects.filter(category_id=category_id, category__name__icontains=query)
            else:
                instance_data = Products.objects.filter(name__icontains=query) | Products.objects.filter(category__name__icontains=query)
            return render(request, 'user/products/search_data.html', {'products_data': instance_data, 'category_id': category_id})

        if request.GET.get('methods') == 'category':
            instance_data = Products.objects.all() if category_id == 'all' else Products.objects.filter(category__id=category_id)
            return render(request, 'user/products/search_data.html', {'products_data': instance_data, 'category_id': category_id})

        return super().get(request, *args, **kwargs)

    
class About_Us(TemplateView):
    template_name = 'user/about_us/about_us.html'


class Careers_Page(FormView):
    form_class = CareersForms
    template_name = 'user/careers/careers.html'
    
    def post(self, request, *args, **kwargs):
        form = CareersForms(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
        
class Contact_Page(FormView):
    form_class = ContactFroms
    template_name = 'user/contact_us/contact_us.html'

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False,'errors': form.errors})
