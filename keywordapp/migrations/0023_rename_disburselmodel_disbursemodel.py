# Generated by Django 3.2 on 2023-07-26 10:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('keywordapp', '0022_disburselmodel'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='DisburselModel',
            new_name='DisburseModel',
        ),
    ]