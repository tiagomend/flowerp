from django import forms
from django.utils.translation import gettext_lazy as _

from warehouse.models import (
    WarehouseType,
    WarehouseAddress,
    Warehouse,
    StorageBin,
    StockMovement,
    MovementType
)

from core.widgets import Awesomplete


class WarehouseTypeForm(forms.ModelForm):
    class Meta:
        model = WarehouseType
        fields = '__all__'


class WarehouseAddressForm(forms.ModelForm):
    class Meta:
        model = WarehouseAddress
        fields = '__all__'


class WarehouseForm(forms.ModelForm):
    class Meta:
        model = Warehouse
        exclude = ['address', 'disabled']


class StorageBinForm(forms.ModelForm):
    class Meta:
        model = StorageBin
        exclude = ['items']


class StockMovementForm(forms.ModelForm):
    class Meta:
        model = StockMovement
        exclude = ['movement_type', 'date', 'tax_invoice', 'service_order', 'purchase_order', 'coust_center']

        widgets = {
            'item': Awesomplete(),
            'warehouse': Awesomplete(),
            'storage_bin': Awesomplete(),
            'stock_uom': Awesomplete(),
        }

class StockMovementInboundForm(forms.ModelForm):
    class Meta:
        model = StockMovement
        fields = ['tax_invoice', 'purchase_order']

        widgets = {
            'purchase_order': Awesomplete(),
        }

class StockMovementOutboundForm(forms.ModelForm):
    class Meta:
        model = StockMovement
        fields = ['tax_invoice', 'service_order', 'coust_center']

        widgets = {
            'service_order': Awesomplete(),
            'coust_center': Awesomplete(),
        }

# Form for filters
class WarehouseTypeFilterForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        label=_('Name'),
        required=False
    )
    description = forms.CharField(
        max_length=100,
        label=_('Description'),
        required=False
    )


class StockMovementFilterForm(forms.Form):
    start_date = forms.DateField(
        widget=forms.TextInput(attrs={'type': 'date'}),
        label=_('Start date'),
        required=False
    )
    end_date = forms.DateField(
        widget=forms.TextInput(attrs={'type': 'date'}),
        label=_('End date'),
        required=False
    )
    product_code = forms.CharField(
        max_length=100,
        label=_('Product code'),
        required=False
    )
    service_order_code = forms.CharField(
        max_length=100,
        label=_('OS'),
        required=False
    )
    movement_type = forms.ChoiceField(
        choices=MovementType.choices,
        label=_('Movement type')
    )


class StorageBinFilterForm(forms.Form):
    ref_position = forms.CharField(
        max_length=100,
        label=_('Bin'),
        required=False
    )
    warehouse = forms.CharField(
        max_length=100,
        label=_('Warehouse'),
        required=False
    )


class StockFilterForm(forms.Form):
    product_name = forms.CharField(
        max_length=100,
        label=_('Product'),
        required=False
    )
    product_code = forms.CharField(
        max_length=100,
        label=_('Code (SKU)'),
        required=False
    )
    storage_bin = forms.CharField(
        max_length=100,
        label=_('Storage Bin'),
        required=False
    )
