# Generated by Django 5.1 on 2024-10-08 13:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('purchase', '0001_initial'),
        ('warehouse', '0004_alter_stockmovement_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='stockmovement',
            name='purchase_order',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='purchase.purchaseorder', verbose_name='Purchase Order'),
        ),
    ]
