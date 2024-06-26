# Generated by Django 3.2 on 2023-08-07 05:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BillDinnerModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bill_online_cash', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('bill_online_cash_count', models.IntegerField(default=0)),
                ('bill_online_card', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('bill_online_card_count', models.IntegerField(default=0)),
                ('pos_ta_bill_phone_cash', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('pos_ta_bill_phone_cash_count', models.IntegerField(default=0)),
                ('pos_ta_bill_phone_card', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('pos_ta_bill_phone_card_count', models.IntegerField(default=0)),
                ('pos_in_bill_cash', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('pos_in_bill_cash_count', models.IntegerField(default=0)),
                ('pos_in_bill_card', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('pos_in_bill_card_count', models.IntegerField(default=0)),
                ('tip_credit', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('wrong_credit', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('edc_in_credit', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('detail_status', models.IntegerField(default=0)),
                ('delivery_cash_count_in_online_system', models.IntegerField(default=0)),
                ('delivery_cash_amount_in_online_system', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('delivery_card_count_in_online_system', models.IntegerField(default=0)),
                ('delivery_card_amount_in_online_system', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('pos_ta_phone_total_bill_count', models.IntegerField(default=0)),
                ('pos_dine_in_total_bill_count', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='BillLunchModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bill_online_cash', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('bill_online_cash_count', models.IntegerField(default=0)),
                ('bill_online_card', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('bill_online_card_count', models.IntegerField(default=0)),
                ('pos_ta_bill_phone_cash', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('pos_ta_bill_phone_cash_count', models.IntegerField(default=0)),
                ('pos_ta_bill_phone_card', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('pos_ta_bill_phone_card_count', models.IntegerField(default=0)),
                ('pos_in_bill_cash', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('pos_in_bill_cash_count', models.IntegerField(default=0)),
                ('pos_in_bill_card', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('pos_in_bill_card_count', models.IntegerField(default=0)),
                ('tip_credit', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('wrong_credit', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('edc_in_credit', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('detail_status', models.IntegerField(default=0)),
                ('pos_ta_phone_total_bill_count', models.IntegerField(default=0)),
                ('pos_dine_in_total_bill_count', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='DisburseModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=100)),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('bill_dinner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='keywordapp.billdinnermodel')),
            ],
        ),
        migrations.CreateModel(
            name='DeliveryDetailModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('delivery_name', models.CharField(default='', max_length=100)),
                ('wage_per_home', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('edc_home_credit', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('moto_credit', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('bill_home_oa_count', models.IntegerField(default=0)),
                ('bill_home_oa_amount', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('bill_home_phone_cash_count', models.IntegerField(default=0)),
                ('bill_home_phone_cash', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('bill_home_phone_card_count', models.IntegerField(default=0)),
                ('bill_home_phone_card', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('bill_home_online_cash_count', models.IntegerField(default=0)),
                ('bill_home_online_cash', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('bill_home_online_card_count', models.IntegerField(default=0)),
                ('bill_home_online_card', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('bill_dinner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='keywordapp.billdinnermodel')),
            ],
        ),
        migrations.CreateModel(
            name='DailyReportModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('bill_dinner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='keywordapp.billdinnermodel')),
                ('bill_lunch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='keywordapp.billlunchmodel')),
            ],
        ),
    ]
