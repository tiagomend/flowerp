from django.utils.translation import gettext as _

from core.presenters import Presenter
from core.html import badge
from warehouse.models import WarehouseType, StockMovement, Stock


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
            self.model.warehouse,
            self.model.storage_bin,
            self.model.get_movement_type_display(),
            self.model.quantity,
            self.model.stock_uom,
            self.model.item_price
        ]

    @property
    def headers(self):
        return [
            _('Date'),
            _('Sku Code'),
            _('Item'),
            _('Warehouse'),
            _('Storage Bin'),
            _('Movement Type'),
            _('Quantity'),
            _('Stock Uom'),
            _('Item Price')
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
            _('Stock Uom'),
            _('Quantity'),
            _('Ordered Qty'),
            _('Reserved Qty'),
        ]
