from django.contrib import admin

from .models import Product, ItemTypeForSped, ProductCategory, UnitOfMeasure


admin.site.register([
    Product,
    ItemTypeForSped,
    ProductCategory,
    UnitOfMeasure
])
