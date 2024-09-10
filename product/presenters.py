from core.presenters import Presenter
from product.models import Product


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
            'Sku code',
            'Name',
            'Unit Of Measure',
            'Item Type For Sped',
            'Price Cost'
        ]
