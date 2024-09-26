from django import forms

from product.models import (
    Product,
    UnitOfMeasure,
    ProductCategory,
    ItemTypeForSped
)


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

        help_texts = {
            'categories': (
                'Mantenha a tecla `Ctrl` pressionada para selecionar ou remover as opções.'
                )
            }


class UnitOfMeasureForm(forms.ModelForm):
    class Meta:
        model = UnitOfMeasure
        fields = '__all__'


class ProductCategoryForm(forms.ModelForm):
    class Meta:
        model = ProductCategory
        fields = '__all__'


class ItemTypeForSpedForm(forms.ModelForm):
    class Meta:
        model = ItemTypeForSped
        fields = '__all__'
