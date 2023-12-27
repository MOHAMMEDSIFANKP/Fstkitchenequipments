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
    def put(self, request, *args, **kwargs):
        print('put methods')
        return super().get(request, *args, **kwargs)

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
        if request.GET.get('methods') == 'search' or request.GET.get('methods') == 'category':
            query = request.GET.get('query', '').strip()    
            category_id = request.GET.get('category_id', '').strip()
            if category_id and category_id != 'all':
                instance_data = Products.objects.filter(category_id=category_id, name__icontains=query) | Products.objects.filter(category_id=category_id, category__name__icontains=query)
            else:
                instance_data = Products.objects.filter(Q(name__icontains=query) | Q(category__name__icontains=query))
            return render(request, 'dashboard/products/search_data.html', {'products_data': instance_data, 'category_id': category_id})

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


class Careers_Dashboard(CustomAuthenticationForm, ListView):
    template_name = 'dashboard/career/career.html'
    context_object_name = 'data_list'
    model = Careers
    ordering = ['-created_at']

    def get(self, request, *args, **kwargs):
        if request.GET.get('methods') == 'search':
            query = request.GET.get('query')
            queryset = Careers.objects.filter(Q(name__icontains = query) | Q(email__icontains=query) | Q(mobile_number__icontains=query) | Q(address__icontains=query))
            return render(request, 'dashboard/career/search_data.html', {'data_list': queryset})
        return super().get(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        form = CareerFilterForm(request.POST)
        if form.is_valid():
            from_date = form.cleaned_data['from_date']
            to_date = form.cleaned_data['to_date']
            queryset = Careers.objects.filter(created_at__date__range=[from_date, to_date])
            return render(request, 'dashboard/career/search_data.html', {'data_list': queryset})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})

class Contacts_dashboard(CustomAuthenticationForm, ListView):
    template_name = 'dashboard/contacts/contacts.html'
    form_class = ContactsFilterForm
    context_object_name = 'data_list'
    model = Contacts
    ordering = ['-created_at']

    def get(self, request, *args, **kwargs):
        if request.GET.get('methods') == 'search':
            query = request.GET.get('query')
            queryset = Contacts.objects.filter(Q(name__icontains = query) | Q(email__icontains=query) | Q(mobile_number__icontains=query) | Q(address__icontains=query) | Q(message__icontains=query) | Q(subject__icontains=query))
            return render(request, 'dashboard/contacts/search_data.html', {'data_list': queryset})
        return super().get(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            from_date = form.cleaned_data['from_date']
            to_date = form.cleaned_data['to_date']
            queryset = Contacts.objects.filter(created_at__date__range=[from_date, to_date])
            return render(request, 'dashboard/contacts/search_data.html', {'data_list': queryset})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})



class About_Dashboard(CustomLoginRequiredAdmin, FormView):
    template_name = 'dashboard/about/about.html'
    form_class = AboutOurStoryForms

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['story_data'] = About_Story.objects.all().first()
        return context
    
    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        pk = request.POST.get('id')
        methods = request.POST.get('methods')

        if pk:
            instance = get_object_or_404(About_Story, pk=pk)
            form = AboutOurStoryForms(request.POST, request.FILES, instance=instance)
        elif pk and methods == 'delete':
            instance = get_object_or_404(About_Story, pk=pk)
            instance.delete()
            return JsonResponse({'success': True})
        else:
            form = AboutOurStoryForms(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})


class Updateviews(UpdateView):
    model = About_Story
    fileds = ['image','body']
    