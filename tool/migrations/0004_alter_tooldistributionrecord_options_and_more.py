# Generated by Django 5.1 on 2024-10-02 13:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('human_resources', '0010_alter_holiday_description'),
        ('tool', '0003_remove_tooldistributionrecord_unique_tool_employee_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tooldistributionrecord',
            options={'verbose_name': 'Tool Distribuition Record'},
        ),
        migrations.AlterField(
            model_name='tooldistributionrecord',
            name='employee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='human_resources.employeehiring', verbose_name='Employee'),
        ),
        migrations.AlterField(
            model_name='tooldistributionrecord',
            name='tool',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='tool.tool', verbose_name='Tool'),
        ),
    ]
