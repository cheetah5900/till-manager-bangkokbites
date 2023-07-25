# Generated by Django 3.2 on 2023-07-25 05:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('keywordapp', '0007_auto_20230725_0315'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='billdinnermodel',
            name='tip_cash',
        ),
        migrations.RemoveField(
            model_name='billlunchmodel',
            name='tip_cash',
        ),
        migrations.AddField(
            model_name='billdinnermodel',
            name='wrong_credit',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='billlunchmodel',
            name='wrong_credit',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]