# Generated by Django 3.2 on 2023-07-19 09:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('keywordapp', '0004_alter_billdinnermodel_edc_home_credit'),
    ]

    operations = [
        migrations.AlterField(
            model_name='billdinnermodel',
            name='edc_home_credit',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]