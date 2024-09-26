from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from tool.views import *


app_name = 'tool'

urlpatterns = [
    path('', ToolIndex.as_view(), name='index'),
    path('new/', CreateTool.as_view(), name='create_tool'),
    path('<int:pk>/', UpdateTool.as_view(), name='update_tool'),
    path('list/', ReadTool.as_view(), name='read_tool'),
    path('categories/new/', CreateToolCategory.as_view(), name='create_category'),
    path('categories/<int:pk>/', UpdateToolCategory.as_view(), name='update_category'),
    path('categories/', ReadToolCategory.as_view(), name='read_category'),
    path('brands/new/', CreateBrand.as_view(), name='create_brand'),
    path('brands/<int:pk>/', UpdateBrand.as_view(), name='update_brand'),
    path('brands/', ReadBrand.as_view(), name='read_brand'),
    path('distributions/new/', CreateToolDistributionRecord.as_view(), name='create_distribution'),
    path('distributions/<int:pk>/', UpdateToolDistributionRecord.as_view(), name='update_distribution'),
    path('distributions/', ReadToolDistributionRecord.as_view(), name='read_distribution'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
