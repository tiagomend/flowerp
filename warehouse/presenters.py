from django.utils.translation import gettext as _

from core.presenters import Presenter
from core.html import badge
from warehouse.models import (
    WarehouseType,
    StockMovement,
    Stock,
    StorageBin,
    Warehouse
)


class WarehouseTypePresenter(Presenter):
    model = WarehouseType

    @property
    def values(self):
        return [
            self.model.name,
            self.model.description if self.model.description else ''
        ]

    @property
    def headers(self):
        return [
            _('Name'),
            _('Description')
        ]


class StockMovementPresenter(Presenter):
    model = StockMovement

    @property
    def values(self):
        return [
            self.model.date,
            self.model.item.sku_code,
            self.model.item.name,
            self.model.warehouse.name,
            self.model.storage_bin.ref_position,
            self.model.get_movement_type_display(),
            self.model.quantity,
            self.model.stock_uom.abbreviation,
            self.model.item_price,
            self.model.service_order.budget_number if self.model.service_order else '',
            self.model.coust_center if self.model.coust_center else '',
        ]

    @property
    def headers(self):
        return [
            _('Date'),
            _('Code (SKU)'),
            _('Item'),
            _('Warehouse'),
            _('Storage Bin'),
            _('Movement Type'),
            _('Quantity'),
            _('UOM'),
            _('Price'),
            _('OS'),
            _('Centro de Custo')
        ]


class StockPresenter(Presenter):
    model = Stock

    @property
    def values(self):
        color = 'success-200' if self.model.quantity > 0 else 'error-100'
        quantity = badge(self.model.quantity, color)

        return [
            self.model.item,
            self.model.storage_bin.warehouse,
            self.model.storage_bin,
            self.model.stock_uom,
            quantity,
            self.model.ordered_qty,
            self.model.reserved_qty
        ]

    @property
    def headers(self):
        return [
            _('Item'),
            _('Warehouse'),
            _('Storage Bin'),
            _('UOM'),
            _('Available'),
            _('Ordered Qty'),
            _('Reserved Qty'),
        ]


class StorageBinPresenter(Presenter):
    model = StorageBin

    @property
    def values(self):
        return [
            self.model.ref_position,
            self.model.warehouse
        ]

    @property
    def headers(self):
        return [
            _('Bin'),
            _('Warehouse')
        ]


class WarehousePresenter(Presenter):
    model = Warehouse

    @property
    def values(self):
        return [
            self.model.name,
            self.model.enterprise,
            self.model.w_type,
            self.model.address,
        ]

    @property
    def headers(self):
        return [
            _('Name'),
            _('Enterprise'),
            _('Warehouse Type'),
            _('Address')
        ]
