from django.shortcuts import render,redirect
from django.views.generic import *
from django.contrib.auth.views import LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib.auth import authenticate,login
from .forms import *
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

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
            return response 

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_superuser:
            return redirect(self.success_url)
        return super().get(request, *args, **kwargs)

class CustomLogoutView(CustomLoginRequiredAdmin,LogoutView):
    template_name = 'dashboard/loginpage.html'
    def get_next_page(self):
        return render(self.request,self.template_name)
    
class DashboardHome(CustomLoginRequiredAdmin,TemplateView):
    template_name = 'dashboard/dashboard.html'

class BackgroudImages(View):
    forms = BgImagesForms()
    template_name = 'dashboard/backgroundimages.html'
    
    def get(self, request, *args, **kwargs):
        conntext = {
            'bgimages_data' : BgImages.objects.all(),
        }
        return render(request, self.template_name, {'form': self.forms,**conntext})

    def post(self, request, *args, **kwargs):
        self.forms = BgImagesForms(request.POST, request.FILES)

        if self.forms.is_valid():
            self.forms.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': self.forms.errors})
        
    def put(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        print(pk,'pk')
        bg_image = get_object_or_404(BgImages, pk=pk)
        self.forms = BgImagesForms(request.POST, request.FILES, instance=bg_image)

        if self.forms.is_valid():
            self.forms.save()
            return JsonResponse({'success': True})
        else:
            errors = {field: self.forms[field].errors for field in self.forms.fields}
            return JsonResponse({'success': False, 'errors': self.forms.errors})
        return
