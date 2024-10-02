from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from service.views import *


app_name = 'service'

urlpatterns = [
    path('orders/new/', CreateServiceOrder.as_view(), name='create_service_order'),
    path('orders/<int:pk>/', UpdateServiceOrder.as_view(), name='update_service_order'),
    path('orders/', ReadServiceOrder.as_view(), name='read_service_order'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
