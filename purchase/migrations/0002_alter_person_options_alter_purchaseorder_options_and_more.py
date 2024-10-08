# Generated by Django 5.1 on 2024-10-09 13:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_enterprise_identification_number'),
        ('purchase', '0001_initial'),
        ('warehouse', '0006_alter_stockmovement_tax_invoice'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='person',
            options={'verbose_name': 'Supplier'},
        ),
        migrations.AlterModelOptions(
            name='purchaseorder',
            options={'ordering': ['-code'], 'verbose_name': 'Purchase Order'},
        ),
        migrations.AlterField(
            model_name='person',
            name='cpf_or_cnpj',
            field=models.CharField(max_length=14, verbose_name='CPF/CNPJ'),
        ),
        migrations.AlterField(
            model_name='person',
            name='is_supplier',
            field=models.BooleanField(default=True, verbose_name='Supplier'),
        ),
        migrations.AlterField(
            model_name='person',
            name='name',
            field=models.CharField(max_length=50, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='person',
            name='person_type',
            field=models.CharField(choices=[('PJ', 'Pessoa Física'), ('PF', 'Pessoa Jurídica')], max_length=50, verbose_name='Person Type'),
        ),
        migrations.AlterField(
            model_name='person',
            name='phone',
            field=models.CharField(blank=True, max_length=14, null=True, verbose_name='Phone'),
        ),
        migrations.AlterField(
            model_name='person',
            name='rg_or_ie',
            field=models.CharField(blank=True, max_length=14, null=True, verbose_name='RG/IE'),
        ),
        migrations.AlterField(
            model_name='purchaseorder',
            name='approval_date',
            field=models.DateField(null=True, verbose_name='Approva Date'),
        ),
        migrations.AlterField(
            model_name='purchaseorder',
            name='code',
            field=models.BigAutoField(primary_key=True, serialize=False, verbose_name='Code'),
        ),
        migrations.AlterField(
            model_name='purchaseorder',
            name='delivery_forecast',
            field=models.DateField(verbose_name='Delivery forecast'),
        ),
        migrations.AlterField(
            model_name='purchaseorder',
            name='discount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Discount'),
        ),
        migrations.AlterField(
            model_name='purchaseorder',
            name='enterprise',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.enterprise', verbose_name='Enterprise'),
        ),
        migrations.AlterField(
            model_name='purchaseorder',
            name='status',
            field=models.CharField(blank=True, choices=[('Draft', 'Rascunho'), ('Approved', 'Aprovado'), ('Rejected', 'Rejeitado'), ('Delivery', 'Para Entrega'), ('Concluded', 'Concluído'), ('Late', 'Entrega Atrasada'), ('Canceled', 'Cancelado')], default='Draft', max_length=9, verbose_name='Status'),
        ),
        migrations.AlterField(
            model_name='purchaseorder',
            name='supplier',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='purchase.person', verbose_name='Supplier'),
        ),
        migrations.AlterField(
            model_name='purchaseorder',
            name='warehouse',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='warehouse.warehouse', verbose_name='Warehouse'),
        ),
    ]
