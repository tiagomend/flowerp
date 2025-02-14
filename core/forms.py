from django import forms

from core.models import Enterprise, CoustCenter

class EnterpriseForm(forms.ModelForm):
    class Meta:
        model = Enterprise
        fields = '__all__'


class CoustCenterForm(forms.ModelForm):
    class Meta:
        model = CoustCenter
        fields = '__all__'
