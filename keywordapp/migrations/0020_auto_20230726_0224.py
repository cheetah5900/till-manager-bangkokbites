# Generated by Django 3.2 on 2023-07-26 02:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('keywordapp', '0019_rename_wage_per_hour_deliverydetailmodel_wage_per_home'),
    ]

    operations = [
        migrations.AddField(
            model_name='deliverydetailmodel',
            name='real_bill_home_online_card',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='deliverydetailmodel',
            name='real_bill_home_online_card_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='deliverydetailmodel',
            name='real_bill_home_online_cash',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='deliverydetailmodel',
            name='real_bill_home_online_cash_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='deliverydetailmodel',
            name='real_bill_home_phone_card',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='deliverydetailmodel',
            name='real_bill_home_phone_card_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='deliverydetailmodel',
            name='real_bill_home_phone_cash',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='deliverydetailmodel',
            name='real_bill_home_phone_cash_count',
            field=models.IntegerField(default=0),
        ),
    ]