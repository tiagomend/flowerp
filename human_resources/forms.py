from django import forms

from core.widgets import Awesomplete
from human_resources.models import (
    EmployeePosition,
    Employee,
    EmployeeHiring,
    Vacation,
    Salary,
    SalaryAdjustment,
    Document
)


class EmployeePositionForm(forms.ModelForm):
    class Meta:
        model = EmployeePosition
        fields = '__all__'


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = '__all__'

        widgets = {
            'position': Awesomplete(),
        }


class EmployeeHiringForm(forms.ModelForm):
    class Meta:
        model = EmployeeHiring
        fields = '__all__'

        widgets = {
            'employee': Awesomplete(),
            'salary': Awesomplete(),
            'admission_date': forms.TextInput(attrs={'type': 'date'}),
            'expiry_of_experience': forms.TextInput(attrs={'type': 'date'}),
            'termination_date': forms.TextInput(attrs={'type': 'date'}),
        }


class EmployeeHiringEditForm(forms.ModelForm):
    class Meta:
        model = EmployeeHiring
        fields = '__all__'

        widgets = {
            'employee': forms.HiddenInput(attrs={'readonly': 'readonly'}),
            'admission_date': forms.TextInput(attrs={'readonly': 'readonly', 'type': 'date'}),
            'expiry_of_experience': forms.TextInput(attrs={'type': 'date'}),
            'termination_date': forms.TextInput(attrs={'type': 'date'}),
        }


class VacationForm(forms.ModelForm):
    class Meta:
        model = Vacation
        fields = '__all__'

        widgets = {
            'employee_hiring': Awesomplete(),
            'start_date': forms.TextInput(attrs={'type': 'date'}),
            'end_date': forms.TextInput(attrs={'type': 'date'})
        }


class SalaryForm(forms.ModelForm):
    class Meta:
        model = Salary
        fields = '__all__'

        widgets = {
            'position': Awesomplete(),
        }


class SalaryAdjustmentForm(forms.ModelForm):
    class Meta:
        model = SalaryAdjustment
        exclude = ['previous_salary']

        widgets = {
            'salary': Awesomplete(),
            'date': forms.TextInput(attrs={'type': 'date'}),
        }


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = '__all__'

        widgets = {
            'employee_hiring': Awesomplete(),
            'issue_date': forms.TextInput(attrs={'type': 'date'}),
            'expiration_date': forms.TextInput(attrs={'type': 'date'}),
        }

    def clean_file(self):
        file = self.cleaned_data.get('file')
        if file:
            if not file.name.endswith('.pdf'):
                raise forms.ValidationError("The file must be in PDF format.")
        return file
