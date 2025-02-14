from django.urls import path

from core.views import *


app_name = 'core'

urlpatterns = [
    path('enterprise/new/', CreateEnterprise.as_view(), name='create_enterprise'),
    path('enterprise/<int:pk>/', UpdateEnterprise.as_view(), name='update_enterprise'),
    path('enterprise/', ReadEnterprise.as_view(), name='read_enterprise'),
    path('coustcenter/new/', CreateCoustCenter.as_view(), name='create_coustcenter'),
    path('coustcenter/<int:pk>/', UpdateCoustCenter.as_view(), name='update_coustcenter'),
    path('coustcenter/', ReadCoustCenter.as_view(), name='read_coustcenter'),
]
