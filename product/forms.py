from django import forms

from product.models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

        help_texts = {
            'categories': (
                'Mantenha a tecla `Ctrl` pressionada para selecionar ou remover as opções.'
                )
            }
