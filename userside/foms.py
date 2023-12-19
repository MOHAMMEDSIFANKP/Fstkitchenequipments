from django.core.exceptions import ValidationError
from django import forms
from dashboard.models import Careers

class CareersForms(forms.ModelForm):
    class Meta:
        model = Careers
        fields = ('name', 'email', 'mobile_number', 'cv', 'address')

    def clean_cv(self):
        cv = self.cleaned_data.get("cv")
        if not cv:
            raise ValidationError('Please upload a cv')  
        allowed_extensions = ['pdf', 'csv', 'doc', 'docx']
        file_extension = cv.name.lower().split('.')[-1]
        if file_extension not in allowed_extensions:
            raise ValidationError('Invalid CV format. Please upload a valid CV.')
        return cv
    