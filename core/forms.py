from django import forms

from core.models import Enterprise

class EnterpriseForm(forms.ModelForm):
    class Meta:
        model = Enterprise
        fields = '__all__'
