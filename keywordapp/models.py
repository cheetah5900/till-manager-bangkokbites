from django.db import models


class BillLunchModel(models.Model):
    bill_online_cash = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)
    bill_online_cash_count = models.IntegerField(default=0)
    bill_online_card = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)
    bill_online_card_count = models.IntegerField(default=0)
    pos_ta_bill_phone_cash = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)
    pos_ta_bill_phone_cash_count = models.IntegerField(default=0)
    pos_ta_bill_phone_card = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)
    pos_ta_bill_phone_card_count = models.IntegerField(default=0)
    pos_in_bill_cash = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)
    pos_in_bill_cash_count = models.IntegerField(default=0)
    pos_in_bill_card = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)
    pos_in_bill_card_count = models.IntegerField(default=0)
    tip_credit = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)
    wrong_credit = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)
    edc_in_credit = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)
    detail_status = models.IntegerField(default=0)
    pos_ta_phone_total_bill_count = models.IntegerField(default=0)
    pos_dine_in_total_bill_count = models.IntegerField(default=0)

    def __str__(self):
        return self.real_bill_phone_cash


class BillDinnerModel(models.Model):
    bill_online_cash = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)
    bill_online_cash_count = models.IntegerField(default=0)
    bill_online_card = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)
    bill_online_card_count = models.IntegerField(default=0)
    pos_ta_bill_phone_cash = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)
    pos_ta_bill_phone_cash_count = models.IntegerField(default=0)
    pos_ta_bill_phone_card = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)
    pos_ta_bill_phone_card_count = models.IntegerField(default=0)
    pos_in_bill_cash = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)
    pos_in_bill_cash_count = models.IntegerField(default=0)
    pos_in_bill_card = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)
    pos_in_bill_card_count = models.IntegerField(default=0)
    tip_credit = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)
    wrong_credit = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)
    edc_in_credit = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)
    detail_status = models.IntegerField(default=0)

    delivery_cash_count_in_online_system = models.IntegerField(default=0)
    delivery_cash_amount_in_online_system = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)
    delivery_card_count_in_online_system = models.IntegerField(default=0)
    delivery_card_amount_in_online_system = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)

    pos_ta_phone_total_bill_count = models.IntegerField(default=0)
    pos_dine_in_total_bill_count = models.IntegerField(default=0)

    def __str__(self):
        return self.real_bill_phone_cash


class DisburseModel(models.Model):
    name = models.CharField(max_length=100, default='')
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    bill_dinner = models.ForeignKey(BillDinnerModel, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class DeliveryDetailModel(models.Model):
    delivery_name = models.CharField(max_length=100, default='')
    wage_per_home = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)
    edc_home_credit = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)
    moto_credit = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)
    bill_home_oa_count = models.IntegerField(default=0)
    bill_home_oa_amount = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)
    bill_home_phone_cash_count = models.IntegerField(default=0)
    bill_home_phone_cash = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)
    bill_home_phone_card_count = models.IntegerField(default=0)
    bill_home_phone_card = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)
    bill_home_online_cash_count = models.IntegerField(default=0)
    bill_home_online_cash = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)
    bill_home_online_card_count = models.IntegerField(default=0)
    bill_home_online_card = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)
    bill_dinner = models.ForeignKey(BillDinnerModel, on_delete=models.CASCADE)

    def __str__(self):
        return self.delivery_name


class DailyReportModel(models.Model):
    date = models.DateField()
    branch = models.CharField(default="cr",max_length=20)
    bill_lunch = models.ForeignKey(BillLunchModel, on_delete=models.CASCADE)
    bill_dinner = models.ForeignKey(BillDinnerModel, on_delete=models.CASCADE)

    def __str__(self):
        return f"Daily Report for {self.date}"
