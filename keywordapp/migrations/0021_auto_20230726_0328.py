# Generated by Django 3.2 on 2023-07-26 03:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('keywordapp', '0020_auto_20230726_0224'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='billdinnermodel',
            name='edc_home_credit',
        ),
        migrations.RemoveField(
            model_name='billdinnermodel',
            name='real_bill_home_online_card',
        ),
        migrations.RemoveField(
            model_name='billdinnermodel',
            name='real_bill_home_online_card_count',
        ),
        migrations.RemoveField(
            model_name='billdinnermodel',
            name='real_bill_home_online_cash',
        ),
        migrations.RemoveField(
            model_name='billdinnermodel',
            name='real_bill_home_online_cash_count',
        ),
        migrations.RemoveField(
            model_name='billdinnermodel',
            name='real_bill_home_phone_card',
        ),
        migrations.RemoveField(
            model_name='billdinnermodel',
            name='real_bill_home_phone_card_count',
        ),
        migrations.RemoveField(
            model_name='billdinnermodel',
            name='real_bill_home_phone_cash',
        ),
        migrations.RemoveField(
            model_name='billdinnermodel',
            name='real_bill_home_phone_cash_count',
        ),
    ]
