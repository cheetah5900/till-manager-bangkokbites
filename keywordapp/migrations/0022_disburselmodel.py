# Generated by Django 3.2 on 2023-07-26 08:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('keywordapp', '0021_auto_20230726_0328'),
    ]

    operations = [
        migrations.CreateModel(
            name='DisburselModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=100)),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('bill_dinner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='keywordapp.billdinnermodel')),
            ],
        ),
    ]