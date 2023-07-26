# Generated by Django 3.2 on 2023-07-25 14:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('keywordapp', '0014_rename_derivery_name_billdinnermodel_delivery_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='deliverydetailmodel',
            old_name='commission',
            new_name='home_commission',
        ),
        migrations.RemoveField(
            model_name='billdinnermodel',
            name='delivery_name',
        ),
        migrations.RemoveField(
            model_name='billdinnermodel',
            name='home_commission',
        ),
        migrations.RemoveField(
            model_name='billdinnermodel',
            name='real_bill_home_oa_amount',
        ),
        migrations.RemoveField(
            model_name='billdinnermodel',
            name='real_bill_home_oa_count',
        ),
        migrations.AddField(
            model_name='billdinnermodel',
            name='delivery_detail',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='keywordapp.deliverydetailmodel'),
        ),
        migrations.AddField(
            model_name='deliverydetailmodel',
            name='real_bill_home_oa_amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='deliverydetailmodel',
            name='real_bill_home_oa_count',
            field=models.IntegerField(default=0),
        ),
    ]
