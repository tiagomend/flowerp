from decimal import Decimal

from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class StorageBinDoesNotBelongWarehouse(ValidationError):
    pass


class NotSufficientBalance(ValidationError):
    pass


class WarehouseType(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)

    def __str__(self) -> str:
        return str(self.name)

    class Meta:
        db_table = 'warehouse_types'


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


class Warehouse(models.Model):
    name = models.CharField(max_length=100)

    enterprise = models.ForeignKey(
        'core.Enterprise',
        on_delete=models.PROTECT,
        null=True,
        blank=True
    )

    w_type = models.ForeignKey(
        'WarehouseType',
        on_delete=models.PROTECT,
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
        return f'W{self.pk} - {self.name}'

    class Meta:
        db_table = 'warehouses'


class StorageBin(models.Model):
    ref_position = models.CharField(max_length=20)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.PROTECT)
    items = models.ManyToManyField('product.Product', through='Stock')

    def __str__(self) -> str:
        return f'{self.ref_position} : W{self.warehouse.pk}'

    class Meta:
        db_table = 'storage_bins'


class Stock(models.Model):
    item = models.ForeignKey('product.Product', on_delete=models.PROTECT)
    storage_bin = models.ForeignKey(StorageBin, on_delete=models.PROTECT)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    ordered_qty = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    reserved_qty = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    stock_uom = models.ForeignKey('product.UnitOfMeasure', on_delete=models.PROTECT)

    class Meta:
        db_table = 'stocks'


class MovementType(models.TextChoices):
    INBOUND = ('in', _('Inbound'))
    OUTBOUND = ('out', _('Outbound'))


class StockMovement(models.Model):
    date = models.DateTimeField()
    movement_type = models.CharField(max_length=3, choices=MovementType.choices)
    item = models.ForeignKey('product.Product', on_delete=models.PROTECT)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.PROTECT)
    storage_bin = models.ForeignKey(StorageBin, on_delete=models.SET_NULL, null=True)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    stock_uom = models.ForeignKey('product.UnitOfMeasure', on_delete=models.PROTECT)
    item_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

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
            self.quantity = int(self.quantity)
            self.quantity *= -1

        if self.item_price == str(0):
            self.item_price = self.item.price_cost

        self.move_stock()

        return super().save(*args, **kwargs)

    class Meta:
        ordering = ['-date']
        db_table = 'stock_movements'
