from django.utils.translation import gettext as _

from core.presenters import Presenter
from product.models import (
    Product,
    UnitOfMeasure,
    ProductCategory,
    ItemTypeForSped
)


class ProductPresenter(Presenter):
    model = Product

    @property
    def values(self):
        model_list = [
            self.model.sku_code,
            self.model.name,
            self.model.unit_of_measure,
            self.model.item_type_for_sped,
            self.model.price_cost
        ]

        return model_list

    @property
    def headers(self):
        return [
            _('Code (SKU)'),
            _('Name'),
            _('Unit Of Measure'),
            _('Item Type For SPED'),
            _('Price Cost')
        ]


class UnitOfMeasurePresenter(Presenter):
    model = UnitOfMeasure

    @property
    def values(self):
        return [
            self.model.name,
            self.model.abbreviation,
        ]

    @property
    def headers(self):
        return [
            _('Name'),
            _('Abbreviation'),
        ]


class ProductCategoryPresenter(Presenter):
    model = ProductCategory

    @property
    def values(self):
        return [
            self.model.name,
            self.model.description,
        ]

    @property
    def headers(self):
        return [
            _('Name'),
            _('Description'),
        ]


class ItemTypeForSpedPresenter(Presenter):
    model = ItemTypeForSped

    @property
    def values(self):
        return [
            self.model.code,
            self.model.description,
        ]

    @property
    def headers(self):
        return [
            _('Code'),
            _('Description'),
        ]
