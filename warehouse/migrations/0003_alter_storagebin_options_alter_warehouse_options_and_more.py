# Generated by Django 5.1 on 2024-10-07 13:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_alter_product_options_alter_productcategory_options_and_more'),
        ('service', '0001_initial'),
        ('warehouse', '0002_warehouse_enterprise_stock_storagebin_stockmovement_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='storagebin',
            options={'verbose_name': 'Storage Bin'},
        ),
        migrations.AlterModelOptions(
            name='warehouse',
            options={'verbose_name': 'Warehouse'},
        ),
        migrations.AddField(
            model_name='stockmovement',
            name='service_order',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='service.serviceorder'),
        ),
        migrations.AddField(
            model_name='stockmovement',
            name='tax_invoice',
            field=models.IntegerField(blank=True, null=True, verbose_name='Tax Invoice'),
        ),
        migrations.AlterField(
            model_name='storagebin',
            name='items',
            field=models.ManyToManyField(through='warehouse.Stock', to='product.product', verbose_name='Items'),
        ),
        migrations.AlterField(
            model_name='storagebin',
            name='ref_position',
            field=models.CharField(max_length=20, verbose_name='Bin'),
        ),
        migrations.AlterField(
            model_name='storagebin',
            name='warehouse',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='warehouse.warehouse', verbose_name='Warehouse'),
        ),
    ]
