from django import forms

from service.models import ServiceOrder


class ServiceOrderForm(forms.ModelForm):
    class Meta:
        model = ServiceOrder
        fields = '__all__'
