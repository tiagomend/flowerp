from django import forms

from purchase.models import PurchaseOrder, PurchaseOrderItems, Person
from core.widgets import Awesomplete


class PurchaseOrderForm(forms.ModelForm):
    class Meta:
        model = PurchaseOrder
        exclude = ['id', 'items', 'approval_date']

        widgets = {
            'enterprise': Awesomplete(),
            'warehouse': Awesomplete(),
            'supplier': Awesomplete(),
            'delivery_forecast': forms.TextInput(attrs={'type': 'date'}),
            'status': forms.Select(attrs={'disabled': True}),
        }


class PurchaseOrderItemsForm(forms.ModelForm):
    class Meta:
        model = PurchaseOrderItems
        exclude = ['id', 'purchase_order']

        widgets = {
            'item': Awesomplete(),
        }


class SupplierForm(forms.ModelForm):
    class Meta:
        model = Person
        exclude = ['principal_address', 'delivery_address', 'id']


class ReportPOForm(forms.Form):
    start_date = forms.DateField(
        label="Data de Início",
        widget=forms.TextInput(
            attrs={
                "type": "date",
            }
        )
    )
    end_date = forms.DateField(
        label="Data de Término",
        widget=forms.TextInput(
            attrs={
                "type": "date",
            }
        )
    )
    code = forms.CharField(
        label="Nº do Pedido",
        max_length=60,
    )
