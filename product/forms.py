from django import forms
from django.utils.translation import gettext_lazy as _

from product.models import (
    Product,
    UnitOfMeasure,
    ProductCategory,
    ItemTypeForSped
)


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ['id']

        help_texts = {
            'categories': (
                'Mantenha a tecla `Ctrl` pressionada para selecionar ou remover as opções.'
                )
            }


class UnitOfMeasureForm(forms.ModelForm):
    class Meta:
        model = UnitOfMeasure
        exclude = ['id']


class ProductCategoryForm(forms.ModelForm):
    class Meta:
        model = ProductCategory
        fields = '__all__'


class ItemTypeForSpedForm(forms.ModelForm):
    class Meta:
        model = ItemTypeForSped
        fields = '__all__'


# Form for filters
class ProductFilterForm(forms.Form):
    name = forms.CharField(max_length=100, label=_('Name'), required=False)
    code = forms.CharField(max_length=100, label=_('Code (SKU)'), required=False)
