# Generated by Django 3.2 on 2023-07-25 11:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('keywordapp', '0012_billdinnermodel_home_commission'),
    ]

    operations = [
        migrations.AddField(
            model_name='billdinnermodel',
            name='derivery_name',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='billdinnermodel',
            name='home_commission',
            field=models.DecimalField(decimal_places=2, default=4, max_digits=10),
        ),
    ]
