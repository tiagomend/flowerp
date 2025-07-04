from decimal import Decimal

from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class StorageBinDoesNotBelongWarehouse(ValidationError):
    pass


class NotSufficientBalance(ValidationError):
    pass


class WarehouseType(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name=_('Name')
    )
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name=_('Description')
    )

    def __str__(self) -> str:
        return str(self.name)

    class Meta:
        db_table = 'warehouse_types'
        verbose_name = _('Warehouse Type')


class StreetType(models.TextChoices):
    AVENUE = ('AV', 'Avenida')
    STREET = ('R', 'Rua')
    PLATE = ('T', 'Travessa')
    FARM = ('FAZ', 'Fazenda')


class WarehouseAddress(models.Model):
    street_type = models.CharField(
        max_length=3,
        choices=StreetType.choices,
        default=StreetType.STREET,
        verbose_name=_('Street type')
    )
    street = models.CharField(
        max_length=100,
        verbose_name=_('Street')
    )
    number = models.CharField(
        max_length=20,
        verbose_name=_('Number')
    )
    complement = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name=_('Complement')
    )
    neighborhood = models.CharField(
        max_length=50,
        verbose_name=_('Neighborhood')
    )
    city = models.CharField(
        max_length=50,
        verbose_name=_('City')
    )
    state = models.CharField(
        max_length=50,
        verbose_name=_('State')
    )
    postal_code = models.CharField(
        max_length=9,
        verbose_name=_('Postal code')
    )

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


class Warehouse(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name=_('Name')
    )

    enterprise = models.ForeignKey(
        'core.Enterprise',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name=_('Enterprise')
    )

    w_type = models.ForeignKey(
        'WarehouseType',
        on_delete=models.PROTECT,
        verbose_name=_('Warehouse Type')
    )

    address = models.ForeignKey(
        'WarehouseAddress',
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name='address'
    )

    disabled = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f'DP{self.pk} - {self.name}'

    class Meta:
        db_table = 'warehouses'
        verbose_name = _('Warehouse')


class StorageBin(models.Model):
    ref_position = models.CharField(
        max_length=20,
        verbose_name=_('Bin')
    )
    warehouse = models.ForeignKey(
        Warehouse,
        on_delete=models.PROTECT,
        verbose_name=_('Warehouse')
    )
    items = models.ManyToManyField(
        'product.Product',
        through='Stock',
        verbose_name=_('Items')
    )

    def __str__(self) -> str:
        return f'{self.ref_position} : DP{self.warehouse.pk}'

    class Meta:
        db_table = 'storage_bins'
        verbose_name = _('Storage Bin')


class Stock(models.Model):
    item = models.ForeignKey(
        'product.Product',
        on_delete=models.PROTECT,
        verbose_name=_('Item')
    )
    storage_bin = models.ForeignKey(
        StorageBin,
        on_delete=models.PROTECT,
        verbose_name=_('Storage Bin')
    )
    quantity = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_('Quantity')
    )
    ordered_qty = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    reserved_qty = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    stock_uom = models.ForeignKey('product.UnitOfMeasure', on_delete=models.PROTECT)

    class Meta:
        db_table = 'stocks'
        verbose_name = _('Stock')


class MovementType(models.TextChoices):
    INBOUND = ('in', _('Inbound'))
    OUTBOUND = ('out', _('Outbound'))


class StockMovement(models.Model):
    date = models.DateTimeField(verbose_name=_('Date'))
    service_order = models.ForeignKey(
        'service.ServiceOrder',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_('Service Order')
    )
    purchase_order = models.ForeignKey(
        'purchase.PurchaseOrder',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_('Purchase Order')
    )
    coust_center = models.ForeignKey(
        'core.CoustCenter',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_('Centro de Custo')
    )
    tax_invoice = models.CharField(
        verbose_name=_('Tax Invoice'),
        null=True,
        blank=True,
        max_length=255
    )
    movement_type = models.CharField(
        max_length=3,
        choices=MovementType.choices,
        verbose_name=_('Movement type'),
    )
    item = models.ForeignKey('product.Product', on_delete=models.PROTECT)
    warehouse = models.ForeignKey(
        Warehouse,
        on_delete=models.PROTECT,
        verbose_name=_('Warehouse')
    )
    storage_bin = models.ForeignKey(
        StorageBin,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name=_('Storage Bin')
    )
    quantity = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_('Quantity')
    )
    stock_uom = models.ForeignKey(
        'product.UnitOfMeasure',
        on_delete=models.PROTECT,
        verbose_name=_('UOM')
    )
    item_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_('Price')
    )

    def get_stock(self):
        if Stock.objects.filter(
                item=self.item,
                storage_bin=self.storage_bin,
                stock_uom=self.stock_uom
            ).exists():

            return Stock.objects.get(
                item=self.item,
                storage_bin=self.storage_bin,
                stock_uom=self.stock_uom
            )

        return None

    def is_valid(self):
        if self.storage_bin.warehouse != self.warehouse:
            raise StorageBinDoesNotBelongWarehouse(
                'Error: The storage bin you specified is not in the warehouse you specified.'
                )

        if self.movement_type == MovementType.OUTBOUND:
            stock = self.get_stock()

            if not stock:
                raise NotSufficientBalance('Inventory does not have sufficient balance.')

            if stock:
                if (stock.quantity + Decimal(self.quantity)) < 0:
                    raise NotSufficientBalance('Inventory does not have sufficient balance.')

        return True

    def move_stock(self):
        stock = self.get_stock()

        if stock:
            if (stock.quantity + Decimal(self.quantity)) < 0:
                raise NotSufficientBalance('Inventory does not have sufficient balance.')

            stock.quantity += Decimal(self.quantity)
            stock.save()

        else:
            Stock.objects.create(
                item=self.item,
                storage_bin=self.storage_bin,
                stock_uom=self.stock_uom,
                quantity=self.quantity
            ).save()

    def save(self, *args, **kwargs) -> None:
        if self.movement_type == MovementType.OUTBOUND:
            self.quantity = float(self.quantity)
            self.quantity *= -1

        if self.item_price == str(0):
            self.item_price = self.item.price_cost

        self.move_stock()

        return super().save(*args, **kwargs)

    class Meta:
        ordering = ['-date']
        db_table = 'stock_movements'
        verbose_name = _('Stock Movement')
