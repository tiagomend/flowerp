# Generated by Django 5.1 on 2024-09-25 11:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('human_resources', '0009_vacation_unique_employee_hiring_start_and_end_date'),
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='ToolCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Tool',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('asset_number', models.CharField(max_length=12, verbose_name='Asset Number')),
                ('serial_number', models.CharField(max_length=12, verbose_name='Serial Number')),
                ('description', models.TextField(verbose_name='Description')),
                ('acquisition_date', models.DateField(verbose_name='Acquisition Date')),
                ('tool_status', models.CharField(choices=[('new', 'New'), ('lightly_used', 'Lightly Used'), ('used', 'Used'), ('worn', 'Worn'), ('broken', 'Broken'), ('under_repair', 'Under Repair'), ('discarded', 'Discarded')], max_length=12, verbose_name='Tool Status')),
                ('brand', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='tool.brand', verbose_name='Brand')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='product.product', verbose_name='Product')),
                ('tool_category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='tool.toolcategory', verbose_name='Tool Category')),
            ],
            options={
                'verbose_name': 'Tool',
                'db_table': 'tools',
            },
        ),
        migrations.CreateModel(
            name='ToolDistributionRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('issue_date', models.DateTimeField(verbose_name='Issue date')),
                ('return_date', models.DateTimeField(blank=True, null=True, verbose_name='Return date')),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='human_resources.employeehiring')),
                ('tool', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='tool.tool')),
            ],
        ),
        migrations.CreateModel(
            name='ToolReturnRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('return_date', models.DateTimeField(verbose_name='Return date')),
                ('tool_distribution', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='tool.tooldistributionrecord')),
            ],
        ),
    ]
