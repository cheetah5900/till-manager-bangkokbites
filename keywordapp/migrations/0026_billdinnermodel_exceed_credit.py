# Generated by Django 3.2 on 2023-07-28 14:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('keywordapp', '0025_billdinnermodel_edc_in_moto_credit'),
    ]

    operations = [
        migrations.AddField(
            model_name='billdinnermodel',
            name='exceed_credit',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
