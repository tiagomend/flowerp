from abc import ABC, abstractmethod

from django.db.models import Model

from core.models import Enterprise


class Presenter(ABC):
    model: Model

    def __init__(self, model) -> None:
        self.model = model

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
    def all(cls, order_by = '-id'):

        models = cls.model.objects.all().order_by(order_by)
        models_list = []
        for model in models:
            models_list.append(cls(model=model))

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
