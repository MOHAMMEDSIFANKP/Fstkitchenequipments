from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from django import forms
from .models import *
from PIL import Image

class CustomAuthenticationForm(AuthenticationForm):
    def clean_field(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        user = authenticate(username=username, password=password)
        
        if user is not None and not user.is_superuser:
            raise ValidationError('You are not authorized to access the dashboard.')
        return cleaned_data
    
class BgImagesForms(forms.ModelForm):
    class Meta:
        model = BgImages
        fields = ('image', 'sub_heading', 'main_heading')

    def clean_image(self):
        image = self.cleaned_data.get("image")
        if not image:
            raise ValidationError('Please upload a image')  
        try:
            with Image.open(image) as img:
                allowed_formats = ['PNG', 'JPEG', 'JPG', 'WEBP', 'SVG']
                if img.format.upper() not in allowed_formats:
                    raise ValidationError('Invalid image format. Please upload a valid image.')

        except Exception as e:
            raise ValidationError('Error reading the image file.')
        return image
    
    def clean_sub_heading(self):
        sub_heading = self.cleaned_data["sub_heading"]
        if not sub_heading or not sub_heading.strip():
            raise ValidationError('This field is required')
        return sub_heading
    
    def clean_main_heading(self):
        main_heading = self.cleaned_data["main_heading"]
        if not main_heading or not main_heading.strip():
            raise ValidationError('This field is required')
        return main_heading
    
class CategoryForms(forms.ModelForm):
    class Meta:
        model = Categories
        fields = ('image','name')
    
    def clean_image(self):
        image = self.cleaned_data.get("image")
        if not image:
            raise ValidationError('Please upload a image')  
        try:
            with Image.open(image) as img:
                allowed_formats = ['PNG', 'JPEG', 'JPG', 'WEBP', 'SVG']
                if img.format.upper() not in allowed_formats:
                    raise ValidationError('Invalid image format. Please upload a valid image.')

        except Exception as e:
            raise ValidationError('Error reading the image file.')
        return image
    
    def clean_name(self):
        name = self.cleaned_data["name"]
        if not name or not name.strip():
            raise ValidationError('This field is required.')
        name = name.upper()
        return name

class ProductFroms(forms.ModelForm):
    class Meta:
        model = Products
        fields = ('image','category','name')

    def clean_image(self):
        image = self.cleaned_data.get("image")
        if not image:
            raise ValidationError('Please upload a image')  
        try:
            with Image.open(image) as img:
                allowed_formats = ['PNG', 'JPEG', 'JPG', 'WEBP', 'SVG']
                if img.format.upper() not in allowed_formats:
                    raise ValidationError('Invalid image format. Please upload a valid image.')

        except Exception as e:
            raise ValidationError('Error reading the image file.')
        return image
    
    def clean_category(self):
        category = self.cleaned_data["category"]
        if not category:
            raise ValidationError('This field is required.')
        return category
    
    def clean_name(self):
        name = self.cleaned_data["name"]
        if not name or not name.strip():
            raise ValidationError('This field is required.')
        name = name.title()
        return name