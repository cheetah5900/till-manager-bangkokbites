# Generated by Django 3.2 on 2023-07-25 15:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('keywordapp', '0017_rename_wageperhr_deliverydetailmodel_wage_per_hour'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='deliverydetailmodel',
            name='home_commission',
        ),
    ]