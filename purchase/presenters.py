from django.utils.translation import gettext as _

from core.presenters import Presenter
from core.html import badge_icon
from purchase.models import PurchaseOrder, Person


class PurchaseOrderPresenter(Presenter):
    model = PurchaseOrder

    @property
    def values(self):
        status = self.model.get_status_display()

        if status == 'Aprovado':
            color = 'primary-100'
            icon = 'approval'
        elif status == 'Concluído':
            color = 'success-100'
            icon = 'task_alt'
        elif status == 'Cancelado':
            color = 'error-100'
            icon = 'block'
        else:
            color = 'warning-100'
            icon = 'pending'

        status_badge = badge_icon(status, color, icon)

        return [
            self.model.code,
            self.model.enterprise,
            self.model.warehouse.name,
            self.model.supplier,
            status_badge,
            self.model.total,
            self.model.approval_date if self.model.approval_date else "Não Aprovado",
        ]

    @property
    def headers(self):
        return [
            _('Code'),
            _('Enterprise'),
            _('Warehouse'),
            _('Supplier'),
            _('Status'),
            _('Total'),
            _('Approval Date')
        ]


class SupplierPresenter(Presenter):
    model = Person

    @property
    def values(self):
        return [
            self.model.name,
            self.model.get_person_type_display(),
            self.model.cpf_or_cnpj,
            self.model.rg_or_ie if self.model.rg_or_ie else '',
            self.model.phone if self.model.phone else '',
            self.model.email if self.model.email else ''
        ]

    @property
    def headers(self):
        return [
            _('Name'),
            _('Person Type'),
            _('CNPJ/CPF'),
            _('RG/IE'),
            _('Phone'),
            _('Email')
        ]

    @classmethod
    def all(cls, q_filter = None, order_by = '-name'):
        if q_filter:
            models = cls.model.objects.filter(q_filter, is_supplier=True).order_by(order_by)
        else:
            models = cls.model.objects.filter(is_supplier=True).order_by(order_by)

        models_list = []
        for model in models:
            models_list.append(cls(model=model))

        return models_list
