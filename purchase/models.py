from uuid import uuid4

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

PERSON_TYPE_CHOICES = [
    ('PJ', 'Pessoa Física'),
    ('PF', 'Pessoa Jurídica')
]

STREET_TYPE = [
    ('AV', 'Avenida'),
    ('R', 'Rua'),
    ('T', 'Travessa'),
    ('FAZ', 'Fazenda'),
]


class Address(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    street_type = models.CharField(
        max_length=3,
        choices=STREET_TYPE,
        default='R',
    )
    street = models.CharField(max_length=100)
    number = models.CharField(max_length=20)
    complement = models.CharField(
        max_length=50,
        blank=True,
        null=True,
    )
    neighborhood = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    postal_code = models.CharField(max_length=9)

    def __str__(self) -> str:
        return (
            f"{self.street_type}. "
            f"{self.street}, "
            f"{self.number}, "
            f"{self.complement} - "
            f"{self.neighborhood}. CEP: "
            f"{self.postal_code}. "
            f"{self.city} - "
            f"{self.state}."
        )


class Person(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    name = models.CharField(
        max_length=50,
        verbose_name=_('Name')
    )
    fantasy_name = models.CharField(max_length=50)
    person_type = models.CharField(
        max_length=50,
        choices=PERSON_TYPE_CHOICES,
        verbose_name=_('Person Type')
    )
    cpf_or_cnpj = models.CharField(
        max_length=14,
        verbose_name=_('CPF/CNPJ')
    )
    rg_or_ie = models.CharField(
        max_length=14,
        null=True,
        blank=True,
        verbose_name=_('RG/IE')
    )
    email = models.EmailField(max_length=50, null=True, blank=True)
    phone = models.CharField(
        max_length=14,
        null=True,
        blank=True,
        verbose_name=_('Phone')
    )
    principal_address = models.ForeignKey(
        'Address', 
        on_delete=models.PROTECT,
        null=True,
        related_name='principal_address'
    )
    delivery_address = models.ForeignKey(
        'Address',
        on_delete=models.SET_NULL,
        null=True,
        related_name='delivery_address'
    )
    is_supplier = models.BooleanField(
        verbose_name=_('Supplier'),
        default=True
    )


    def __str__(self) -> str:
        return f'{self.cpf_or_cnpj} - {self.fantasy_name}'

    class Meta:
        verbose_name = _('Supplier')


STATUS_CHOICE = [
    ('Draft', 'Rascunho'),
    ('Approved', 'Aprovado'),
    ('Rejected', 'Rejeitado'),
    ('Delivery', 'Para Entrega'),
    ('Concluded', 'Concluído'),
    ('Late', 'Entrega Atrasada'),
    ('Canceled', 'Cancelado'),
]

class PurchaseOrder(models.Model):
    code = models.BigAutoField(
        primary_key=True,
        verbose_name=_('Code')
    )
    id = models.UUIDField(
        unique=True,
        default=uuid4
    )
    enterprise = models.ForeignKey(
        'core.Enterprise',
        on_delete=models.PROTECT,
        verbose_name=_('Enterprise')
    )
    warehouse = models.ForeignKey(
        'warehouse.Warehouse',
        on_delete=models.PROTECT,
        verbose_name=_('Warehouse')
    )
    supplier = models.ForeignKey(
        Person,
        on_delete=models.PROTECT,
        verbose_name=_('Supplier')
    )
    status = models.CharField(
        max_length=9,
        choices=STATUS_CHOICE,
        default='Draft',
        blank=True,
        verbose_name=_('Status')
    )
    items = models.ManyToManyField('product.Product', through='PurchaseOrderItems')
    delivery_forecast = models.DateField(
        verbose_name=_('Delivery forecast')
    )
    approval_date = models.DateField(
        null=True,
        verbose_name=_('Approva Date')
    )
    discount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_('Discount')
    )

    class Meta:
        ordering = ['-code']
        verbose_name = _('Purchase Order')

    def __str__(self) -> str:
        return f"{self.code} - {self.supplier.fantasy_name}"

    @property
    def poitems(self):
        return self.purchaseorderitems_set.all()

    def is_approved(self):
        return self.status == 'Approved'

    def is_concluded(self):
        return self.status == 'Concluded'

    def is_canceled(self):
        return self.status == 'Canceled'

    def approve(self):
        if self.status == 'Draft':
            self.status = 'Approved'
            self.approval_date = timezone.now()
            self.save()

    def cancel(self):
        if self.status in ['Draft', 'Approved']:
            self.status = 'Canceled'
            self.approval_date = None
            self.save()

    def conclude(self):
        if self.status in ['Approved']:
            self.status = 'Concluded'
            self.save()

    def complete_purchase(self):
        self.status = 'Concluded'
        self.save()

    def calculate_total(self):
        total = 0
        items = self.purchaseorderitems_set.all()

        for item in items:
            total = total + item.subtotal()

        return total - self.discount

    @property
    def total(self):
        return f"R$ {round(self.calculate_total(), 2)}".replace('.', ',')

    def put_in_table(self):

        return {
            "head": [
                "Código",
                "Empresa",
                "Depósito",
                "Fornecedor",
                "Situação",
                "Total (R$)",
                "Aprovado em",
            ],
            "row": [
                self.code,
                self.company,
                self.warehouse,
                self.supplier,
                self.status_diplay,
                self.total,
                self.approval_date if self.approval_date else "Não Aprovado",
            ]
        }


class PurchaseOrderItems(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    item = models.ForeignKey('product.Product', on_delete=models.PROTECT)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    freight = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    purchase_order = models.ForeignKey('PurchaseOrder', on_delete=models.PROTECT, blank=True)

    def subtotal(self):
        return (self.unit_price * self.quantity) + self.freight

    @property
    def subtotal_display(self):
        return f"R$ {round(self.subtotal(), 2)}".replace('.', ',')

    @property
    def put_in_table(self):
        return {
            "head": [
                "Item",
                "Quantidade",
                "Unitário (R$)",
                "Frete",
                "Subtotal (R$)",
            ],
            "row": [
                self.item,
                self.quantity,
                self.unit_price,
                self.freight,
                self.subtotal_display,
            ]
        }
