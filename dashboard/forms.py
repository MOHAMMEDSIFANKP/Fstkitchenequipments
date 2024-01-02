from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from django import forms
from .models import *
from PIL import Image
from ckeditor.widgets import CKEditorWidget


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
        sub_heading = sub_heading.upper()
        return sub_heading
    
    def clean_main_heading(self):
        main_heading = self.cleaned_data["main_heading"]
        if not main_heading or not main_heading.strip():
            raise ValidationError('This field is required')
        main_heading = main_heading.upper()
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
        fields = ('image1', 'image2', 'image3', 'category', 'name', 'descrption')

    def clean_image1(self):
        return self.clean_image('image1')

    def clean_image2(self):
        return self.clean_image('image2')

    def clean_image3(self):
        return self.clean_image('image3')

    def clean_image(self, field_name):
        image = self.cleaned_data.get(field_name)

        if not image and field_name == 'image1':
            raise ValidationError('This field is required.')

        if image:
            try:
                with Image.open(image) as img:
                    allowed_formats = ['PNG', 'JPEG', 'JPG', 'WEBP', 'SVG']
                    if img.format.upper() not in allowed_formats:
                        raise ValidationError(f'Invalid image format for {field_name}. Please upload a valid image.')
            except Exception as e:
                raise ValidationError(f'Error reading the image file for {field_name}.')

        return image

    def clean_name(self):
        name = self.cleaned_data["name"]
        if not name or not name.strip():
            raise ValidationError('This field is required.')
        name = name.title()
        return name

    def clean_category(self):
        category = self.cleaned_data["category"]
        if not category:
            raise ValidationError('This field is required.')
        return category
    
 
    
    def clean_descrption(self):
        descrption = self.cleaned_data["descrption"]
        if not descrption or not descrption.strip():
            raise ValidationError('This field is required.')
        descrption = descrption.capitalize()
        return descrption
    
    
class ClientsForms(forms.ModelForm):
    class Meta:
        model = Clients
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

class CareerFilterForm(forms.Form):
    from_date = forms.DateField(label='From Date')
    to_date = forms.DateField(label='To Date')

    def clean(self):
        cleaned_data = super().clean()
        from_date = cleaned_data.get('from_date')
        to_date = cleaned_data.get('to_date')

        if from_date and to_date:
            if from_date > to_date:
                raise forms.ValidationError('From Date must be less than or equal to To Date.')
        return cleaned_data

class ContactsFilterForm(forms.Form):
    from_date = forms.DateField(label='From Date')
    to_date = forms.DateField(label='To Date')

    def clean(self):
        cleaned_data = super().clean()
        from_date = cleaned_data.get('from_date')
        to_date = cleaned_data.get('to_date')

        if from_date and to_date:
            if from_date > to_date:
                raise forms.ValidationError('From Date must be less than or equal to To Date.')
        return cleaned_data


