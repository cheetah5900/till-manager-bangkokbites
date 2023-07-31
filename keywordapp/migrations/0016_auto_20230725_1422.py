# Generated by Django 3.2 on 2023-07-25 14:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('keywordapp', '0015_auto_20230725_1419'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='billdinnermodel',
            name='delivery_detail',
        ),
        migrations.AddField(
            model_name='deliverydetailmodel',
            name='bill_dinner',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='keywordapp.billdinnermodel'),
            preserve_default=False,
        ),
    ]