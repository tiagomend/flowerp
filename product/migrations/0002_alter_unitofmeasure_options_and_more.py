# Generated by Django 5.1 on 2024-10-02 14:20

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='unitofmeasure',
            options={'verbose_name': 'Unit Of Measure'},
        ),
        migrations.AlterField(
            model_name='unitofmeasure',
            name='abbreviation',
            field=models.CharField(max_length=8, verbose_name='Abbreviation'),
        ),
        migrations.AlterField(
            model_name='unitofmeasure',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='unitofmeasure',
            name='name',
            field=models.CharField(max_length=30, verbose_name='Name'),
        ),
    ]