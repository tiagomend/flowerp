from django.db import models


class ItemTypeForSped(models.Model):
    code = models.IntegerField(primary_key=True)
    description = models.CharField(max_length=20)

    class Meta:
        db_table = 'item_types_for_sped'

    def __str__(self) -> str:
        return f'{self.code} - {self.description}'


class UnitOfMeasure(models.Model):
    name = models.CharField(max_length=30)
    abbreviation = models.CharField(max_length=8)

    class Meta:
        db_table = 'units_of_measure'

    def __str__(self) -> str:
        return f'{self.abbreviation} - {self.name}'


class ProductCategory(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'product_categories'

    def __str__(self) -> str:
        return f'{self.name}'


class Product(models.Model):
    sku_code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=50)
    categories = models.ManyToManyField(ProductCategory, blank=True)
    unit_of_measure = models.ForeignKey(UnitOfMeasure, on_delete=models.PROTECT)
    item_type_for_sped = models.ForeignKey(ItemTypeForSped, on_delete=models.PROTECT)
    price_cost = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'products'

    def __str__(self) -> str:
        return f'{self.sku_code} - {self.name}'
