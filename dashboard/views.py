from django.shortcuts import render,redirect
from django.views.generic import *
from django.contrib.auth.views import LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib.auth import authenticate,login
from .forms import *
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.db.models import Q

# Create your views here.

class CustomLoginRequiredAdmin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if not request.user.is_superuser:
                return redirect('Signin')
        else:
            return redirect('Signin')
        return super().dispatch(request, *args, **kwargs)

class Signin(FormView):
    success_url = reverse_lazy('DashboardHome')
    form_class = CustomAuthenticationForm
    template_name = 'dashboard/loginpage.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)

        if user is not None and user.is_superuser:
            login(self.request, user)
            return JsonResponse({'success': True})
        
        
    def form_invalid(self, form):
        response = super().form_invalid(form)
        return JsonResponse({'success': False, 'errors': form.errors})
    

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_superuser:
            return redirect(self.success_url)
        return super().get(request, *args, **kwargs)

class CustomLogoutView(CustomLoginRequiredAdmin,LogoutView):
    template_name = 'dashboard/loginpage.html'
    def get_next_page(self):
        return super().get_next_page()
    
class DashboardHome(CustomLoginRequiredAdmin,TemplateView):
    template_name = 'dashboard/dashboard.html'

class BackgroudImages(CustomLoginRequiredAdmin,FormView):
    template_name = 'dashboard/backgroundimages/backgroundimages.html'
    form_class = BgImagesForms

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['bgimages_data'] = BgImages.objects.all()
        return context
    
    def get(self, request, *args, **kwargs):
        if request.GET.get('methods') == 'search':
            query = request.GET.get('query', '').strip()
            instance_data = BgImages.objects.filter(Q(sub_heading__icontains=query) | Q(main_heading__icontains=query))
            return render(request, 'dashboard/backgroundimages/search_data.html', {'bgimages_data': instance_data})
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        pk = request.POST.get('id')
        methods = request.POST.get('methods')

        if pk and methods == 'put':
            instance = get_object_or_404(BgImages, pk=pk)
            form = BgImagesForms(request.POST, request.FILES, instance=instance)
        elif pk and methods == 'delete':
            instance = get_object_or_404(BgImages, pk=pk)
            instance.delete()
            return JsonResponse({'success': True})
        else:
            form = BgImagesForms(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
        

class Category(CustomLoginRequiredAdmin,FormView):
    template_name = 'dashboard/category/category.html'
    form_class = CategoryForms

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_data'] = Categories.objects.all()
        return context

    def get(self, request, *args, **kwargs):
        if request.GET.get('methods') == 'search':
            query = request.GET.get('query', '').strip()
            instance_data = Categories.objects.filter(name__icontains=query)
            return render(request, 'dashboard/category/search_data.html', {'category_data': instance_data})

        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        pk = request.POST.get('id')
        methods = request.POST.get('methods')

        if pk and methods == 'put':
            instance = get_object_or_404(Categories, pk=pk)
            form = CategoryForms(request.POST, request.FILES, instance=instance)
        elif pk and methods == 'delete':
            instance = get_object_or_404(Categories, pk=pk)
            instance.delete()
            return JsonResponse({'success': True})
        else:
            form = CategoryForms(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})

class Product(CustomLoginRequiredAdmin,FormView):
    template_name = 'dashboard/products/products.html'
    form_class = ProductFroms

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products_data'] = Products.objects.all()
        context['category_data'] = Categories.objects.all().order_by('name')
        return context

    def get(self, request, *args, **kwargs):
        if request.GET.get('methods') == 'search':
            query = request.GET.get('query', '').strip()    
            instance_data = Products.objects.filter(Q(name__icontains=query) | Q(category__name__icontains=query))
            return render(request, 'dashboard/products/search_data.html', {'products_data': instance_data})

        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        pk = request.POST.get('id')
        methods = request.POST.get('methods')

        if pk and methods == 'put':
            instance = get_object_or_404(Products, pk=pk)
            form = ProductFroms(request.POST, request.FILES, instance=instance)
        elif pk and methods == 'delete':
            instance = get_object_or_404(Products, pk=pk)
            instance.delete()
            return JsonResponse({'success': True})
        else:
            form = ProductFroms(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})

class Clients_View(CustomLoginRequiredAdmin,FormView):
    template_name = 'dashboard/clients/clients.html'
    form_class = ClientsForms
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['clients_data'] = Clients.objects.all().order_by('-id')
        return context

    def get(self, request, *args, **kwargs):
        if request.GET.get('methods') == 'search':
            query = request.GET.get('query', '').strip()    
            instance_data = Clients.objects.filter(name__icontains=query)
            return render(request, 'dashboard/clients/search_data.html', {'clients_data': instance_data})

        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        pk = request.POST.get('id')
        methods = request.POST.get('methods')

        if pk and methods == 'put':
            instance = get_object_or_404(Clients, pk=pk)
            form = ClientsForms(request.POST, request.FILES, instance=instance)
        elif pk and methods == 'delete':
            instance = get_object_or_404(Clients, pk=pk)
            instance.delete()
            return JsonResponse({'success': True})
        else:
            form = ClientsForms(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
        