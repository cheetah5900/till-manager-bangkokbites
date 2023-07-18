from django.db import models
    
     
class RealBillModel(models.Model):
    real_bill_phone_cash = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    real_bill_phone_cash_count = models.IntegerField(default=0)
    real_bill_phone_card = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    real_bill_phone_card_count = models.IntegerField(default=0)
    real_bill_online_cash = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    real_bill_online_cash_count = models.IntegerField(default=0)
    real_bill_online_card = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    real_bill_online_card_count = models.IntegerField(default=0)
    real_bill_in_cash = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    real_bill_in_cash_count = models.IntegerField(default=0)
    real_bill_in_card = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    real_bill_in_card_count = models.IntegerField(default=0)
    pos_ta_bill_phone_cash = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    pos_ta_bill_phone_cash_count = models.IntegerField(default=0)
    pos_ta_bill_phone_card = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    pos_ta_bill_phone_card_count = models.IntegerField(default=0)
    pos_in_bill_cash = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    pos_in_bill_cash_count = models.IntegerField(default=0)
    pos_in_bill_card = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    pos_in_bill_card_count = models.IntegerField(default=0)
    edc_in_credit = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    detail_status = models.IntegerField(default=0)

    def __str__(self):
        return self.real_bill_phone_cash
    

class EdcDetailModel(models.Model):
    credit = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    type = models.CharField(max_length=100)
    detail_status = models.IntegerField(default=0)

    def __str__(self):
        return f"EDC Detail {self.pk}"
    
class PosDetailModel(models.Model):
    cash_count = models.IntegerField(default=0)
    cash_amount = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    card_count = models.IntegerField(default=0)
    card_amount = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    pos_type = models.CharField(max_length=100)
    checkout_status = models.IntegerField(default=0)
    detail_status = models.IntegerField(default=0)

    def __str__(self):
        return f"POS Detail {self.pk}"
    
class DeliveryDetailModel(models.Model):
    delivery_name = models.CharField(max_length=100,default='')
    commission = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    wageperhr = models.DecimalField(max_digits=10, decimal_places=2,default=0)

    def __str__(self):
        return self.delivery_name

class DailyReportModel(models.Model):
    date = models.DateField()
    real_bill = models.ForeignKey(RealBillModel, on_delete=models.CASCADE)
    pos_detail = models.ForeignKey(PosDetailModel, on_delete=models.CASCADE)
    edc_detail = models.ForeignKey(EdcDetailModel, on_delete=models.CASCADE)
    delivery_detail = models.ForeignKey(DeliveryDetailModel, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"Daily Report for {self.date}"