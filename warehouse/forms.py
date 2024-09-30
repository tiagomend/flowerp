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
        exclude = ['movement_type', 'date']

        widgets = {
            'item': Awesomplete(),
            'warehouse': Awesomplete(),
            'storage_bin': Awesomplete(),
            'stock_uom': Awesomplete(),
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
    movement_type = forms.ChoiceField(
        choices=MovementType.choices,
        label=_('Movement type')
    )
