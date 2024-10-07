from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from warehouse.views import *


app_name = 'warehouse'

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('new/', CreateWarehouse.as_view(), name='create_warehouse'),
    path('<int:pk>/', UpdateWarehouse.as_view(), name='update_warehouse'),
    path('type/', ReadWarehouseType.as_view(), name='read_w_type'),
    path('type/new/', CreateWarehouseType.as_view(), name='create_w_type'),
    path('type/<int:pk>/', UpdateWarehouseType.as_view(), name='update_w_type'),
    path('storages/new/', CreateStorageBin.as_view(), name='create_storage_bin'),
    path('storages/<int:pk>/', UpdateStorageBin.as_view(), name='update_storage_bin'),
    path('storages/', ReadStorageBin.as_view(), name='read_storage_bin'),
    path('inbound/new/', StockInbound.as_view(), name='stock_inbound'),
    path('inbound/session/', StockInboundSession.as_view(), name='stock_inbound_session'),
    path('inbound/session/clean', StockInboundSessionClean.as_view(), name='stock_inbound_session_clean'),
    path('movements/', ReadStockMovements.as_view(), name='read_stock_movements'),
    path('outbound/new/', StockOutbound.as_view(), name='stock_outbound'),
    path('outbound/session/', StockOutboundSession.as_view(), name='stock_outbound_session'),
    path('outbound/session/clean', StockOutboundSessionClean.as_view(), name='stock_outbound_session_clean'),
    path('movements/', ReadStockMovements.as_view(), name='read_stock_movements'),
    path('stocks/', ReadStock.as_view(), name='read_stock'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
