from django.urls import path

from purchase.views import *

app_name = 'purchase'

urlpatterns = [
    path(
        '',
        Index.as_view(),
        name='index'
    ),
    path(
        'order/new/',
        StartPurchaseOrder.as_view(),
        name='start_purchase_order'
    ),
    path(
        'order/approve/',
        ApprovePurchaseOrder.as_view(),
        name='approve_purchase_order',
    ),
    path(
        'order/cancel/',
        CancelPurchaseOrder.as_view(),
        name='cancel_purchase_order',
    ),
    path(
        'order/conclude/',
        ConcludePurchaseOrder.as_view(),
        name='conclude_purchase_order',
    ),
    path(
        'order/receive/',
        ReceivePurchaseOrder.as_view(),
        name='receive_purchase_order',
    ),
    path(
        'order/report/',
        ReportPurchaseOrder.as_view(),
        name='report_purchase_order',
    ),
    path(
        'order/<str:id>/',
        PurchaseOrderView.as_view(),
        name='purchase_order_view',
    ),
    path(
        'order/save/<str:id>/',
        SavePurchaseOrder.as_view(),
        name='save_purchase_order',
    ),
    path(
        'order/item/<str:id>/',
        DeletePurchaseItem.as_view(),
        name='delete_purchase_item',
    ),
    path(
        'order/item-update/<str:pk>/',
        UpdatePurchaseOrderItem.as_view(),
        name='update_purchase_item',
    ),
    path(
        'order/',
        ReadPurchaseOrder.as_view(),
        name='read_purchase_order',
    ),
    path(
        'supplier/new/',
        CreateSupplier.as_view(),
        name='create_supplier',
    ),
    path(
        'supplier/<str:pk>/',
        UpdateSupplier.as_view(),
        name='update_supplier',
    ),
    path(
        'supplier/',
        ReadSupplier.as_view(),
        name='read_supplier',
    ),
    
]
