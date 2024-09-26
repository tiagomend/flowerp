from django.urls import path

from product.views import *


app_name = 'product'

urlpatterns = [
    path('new/', CreateProduct.as_view(), name='create_product'),
    path('', ReadProduct.as_view(), name='read_product'),
    path('<int:pk>/', UpdateProduct.as_view(), name='update_product'),
    path('uom/new/', CreateUnitOfMeasure.as_view(), name='create_uom'),
    path('uom/', ReadUnitOfMeasure.as_view(), name='read_uom'),
    path('uom/<int:pk>/', UpdateUnitOfMeasure.as_view(), name='update_uom'),
    path('categories/new/', CreateProductCategory.as_view(), name='create_category'),
    path('categories/', ReadProductCategory.as_view(), name='read_category'),
    path('categories/<int:pk>/', UpdateProductCategory.as_view(), name='update_category'),
    path('type/new/', CreateItemTypeForSped.as_view(), name='create_item_type'),
    path('type/', ReadItemTypeForSped.as_view(), name='read_item_type'),
    path('type/<int:pk>/', UpdateItemTypeForSped.as_view(), name='update_item_type'),
]
