# Generated by Django 3.2 on 2023-09-04 03:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('keywordapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='dailyreportmodel',
            name='branch',
            field=models.CharField(default='cr', max_length=20),
        ),
    ]