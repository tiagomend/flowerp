from django.db import models
from django.utils.translation import gettext_lazy as _


class ServiceOrder(models.Model):
    budget_number =  models.IntegerField(verbose_name=_('Budget number'))
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('Price'))
    description = models.TextField(verbose_name=_('Description'))

    class Meta:
        db_table = 'service_orders'
        verbose_name = _('Service Order')
