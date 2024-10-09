from django.utils.translation import gettext as _

from core.presenters import Presenter
from service.models import ServiceOrder

class ServiceOrderPresenter(Presenter):
    model = ServiceOrder

    @property
    def values(self):
        return [
            self.model.budget_number,
            self.model.price,
            self.model.header
        ]

    @property
    def headers(self):
        return [
            _('Budget number'),
            _('Price'),
            _('Header')
        ]
