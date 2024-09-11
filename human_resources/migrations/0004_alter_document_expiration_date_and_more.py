# Generated by Django 5.1 on 2024-09-11 17:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('human_resources', '0003_salary_unique_position_level_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='expiration_date',
            field=models.DateField(blank=True, null=True, verbose_name='Expiration date'),
        ),
        migrations.AlterField(
            model_name='document',
            name='issue_date',
            field=models.DateField(blank=True, null=True, verbose_name='Issue date'),
        ),
    ]
