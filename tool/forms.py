from django import forms

from core.widgets import Awesomplete

from tool.models import (
    ToolCategory,
    Brand,
    Tool,
    ToolDistributionRecord
)


class ToolCategoryForm(forms.ModelForm):
    class Meta:
        model = ToolCategory
        fields = '__all__'


class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = '__all__'


class ToolForm(forms.ModelForm):
    class Meta:
        model = Tool
        fields = '__all__'

        widgets = {
            'item': Awesomplete(),
            'brand': Awesomplete(),
            'tool_category': Awesomplete(),
            'acquisition_date': forms.TextInput(attrs={'type': 'date'}),
        }


class ToolDistributionRecordForm(forms.ModelForm):
    class Meta:
        model = ToolDistributionRecord
        exclude = ['return_date']

        widgets = {
            'tool': Awesomplete(),
            'employee': Awesomplete(),
            'issue_date': forms.TextInput(attrs={'type': 'datetime-local'}),
        }
