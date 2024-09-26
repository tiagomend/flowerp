from django import forms

from warehouse.models import (
    WarehouseType,
    WarehouseAddress,
    Warehouse,
    StorageBin,
    StockMovement
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
