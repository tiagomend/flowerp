from django.urls import path

from product.views import CreateProduct, UpdateProduct, ReadProduct


app_name = 'product'

urlpatterns = [
    path('new/', CreateProduct.as_view(), name='create_product'),
    path('', ReadProduct.as_view(), name='read_product'),
    path('<int:pk>/', UpdateProduct.as_view(), name='update_product'),
]
