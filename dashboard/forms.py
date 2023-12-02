from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from django import forms

class CustomAuthenticationForm(AuthenticationForm):
    def clean_field(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        user = authenticate(username=username, password=password)
        
        if user is not None and not user.is_superuser:
            raise ValidationError('You are not authorized to access the dashboard.')
        return cleaned_data