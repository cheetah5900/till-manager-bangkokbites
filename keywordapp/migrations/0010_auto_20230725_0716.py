# Generated by Django 3.2 on 2023-07-25 07:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('keywordapp', '0009_auto_20230725_0708'),
    ]

    operations = [
        migrations.AddField(
            model_name='billdinnermodel',
            name='real_bill_dinein_dividepay_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='billdinnermodel',
            name='real_bill_taphone_dividepay_count',
            field=models.IntegerField(default=0),
        ),
    ]