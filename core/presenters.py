from abc import ABC, abstractmethod

from django.db.models import Model
from django.core.paginator import Paginator

from core.models import Enterprise, CoustCenter


class Presenter(ABC):
    model: Model

    def __init__(self, model, page_obj = None) -> None:
        self.model = model
        self.page_obj = page_obj

    @property
    @abstractmethod
    def values(self):
        pass

    @property
    @abstractmethod
    def headers(self):
        pass

    @property
    def get_pk(self):
        return self.model.pk

    @classmethod
    def all(cls, request, q_filter = None, order_by = '-id'):
        if q_filter:
            models = cls.model.objects.filter(q_filter).order_by(order_by)
        else:
            models = cls.model.objects.all().order_by(order_by)

        paginator = Paginator(models, 30)
        object = paginator.get_page(request.GET.get('page'))
        models_list = []

        is_first = True
        for model in object:
            if is_first:
                models_list.append(cls(model=model, page_obj=object))
            else:
                models_list.append(cls(model=model))
            is_first = False

        return models_list


class EnterprisePresenter(Presenter):
    model = Enterprise

    @property
    def values(self):
        return [
            self.model.identification_number,
            self.model.corporate_reason,
            self.model.trade_name,
        ]

    @property
    def headers(self):
        return [
            'Identification Number',
            'Corporate Reason',
            'Trade Name',
        ]


class CoustCenterPresenter(Presenter):
    model = CoustCenter

    @property
    def values(self):
        return [
            self.model.name
        ]

    @property
    def headers(self):
        return [
            'Nome'
        ]
