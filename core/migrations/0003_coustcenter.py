# Generated by Django 5.1 on 2025-02-14 10:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_enterprise_identification_number'),
    ]

    operations = [
        migrations.CreateModel(
            name='CoustCenter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
    ]
