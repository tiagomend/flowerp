# Generated by Django 5.1 on 2024-09-11 19:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('human_resources', '0004_alter_document_expiration_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employeehiring',
            name='employee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='human_resources.employee', verbose_name='Employee'),
        ),
        migrations.AlterField(
            model_name='employeehiring',
            name='salary',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='human_resources.salary', verbose_name='Position'),
        ),
    ]
