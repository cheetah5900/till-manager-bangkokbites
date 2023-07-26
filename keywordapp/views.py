
# =============================== FOR PAGE KEYWORD MANAGER ===============================
# =============================== FOR PAGE KEYWORD MANAGER ===============================
# =============================== FOR PAGE KEYWORD MANAGER ===============================

from django.shortcuts import render, redirect,get_object_or_404
from django.urls import reverse
from django.utils import timezone

from decimal import Decimal


from django.contrib.humanize.templatetags.humanize import intcomma

# require login to enter function
# import model
from keywordapp.models import *

# =============================== GENERAL FUNCTION ===============================
# =============================== GENERAL FUNCTION ===============================
# =============================== GENERAL FUNCTION ===============================
def Index(request):
    context = {}
    current_date = timezone.now().date()

    context['current_date'] = current_date
    

    if request.method == 'POST':
        data = request.POST.copy()
        choose_date = data.get('choose_date')
        mode = data.get('mode')

        try:
            daily_report = DailyReportModel.objects.get(date=choose_date)
        except DailyReportModel.DoesNotExist:
            # create empty record
            bill_lunch =  BillLunchModel.objects.create()
            bill_dinner =  BillDinnerModel.objects.create()


            # get last id
            bill_lunch_id = bill_lunch.id
            bill_dinner_id = bill_dinner.id

            # create daily report
            daily_report = DailyReportModel.objects.create(
                date=choose_date,
                bill_lunch_id=bill_lunch_id,
                bill_dinner_id=bill_dinner_id,
            )
            
        if mode == 'lunch':
            return redirect(reverse('lunch-input-quick', kwargs={'daily_report_id': daily_report.id}))
        if mode == 'home':
            return redirect(reverse('home-list', kwargs={'daily_report_id': daily_report.id}))
        if mode == 'dinner':
            return redirect(reverse('dinner-input-quick', kwargs={'daily_report_id': daily_report.id}))


    return render(request, 'keywordapp/index.html', context)

def LunchInputQuick(request,daily_report_id):

    daily_object = get_object_or_404(DailyReportModel, id=daily_report_id)
    date = daily_object.date
    bill_lunch_id = daily_object.bill_lunch.id

    bill_lunch =  BillLunchModel.objects.get(id=bill_lunch_id)

    if request.method == 'POST':
        realBillOnlineCard = request.POST.get('real_bill_online_card')
        posTABillPhoneCard = request.POST.get('pos_ta_bill_phone_card')
        posInCard = request.POST.get('pos_in_bill_card')
        edcInCredit = request.POST.get('edc_in_credit')
        tipCredit = request.POST.get('tip_credit')
        wrongCredit = request.POST.get('wrong_credit')

        bill_lunch =  get_object_or_404(BillLunchModel, id=bill_lunch_id)
        bill_lunch.real_bill_online_card = realBillOnlineCard
        bill_lunch.pos_ta_bill_phone_card = posTABillPhoneCard
        bill_lunch.pos_in_bill_card = posInCard
        bill_lunch.edc_in_credit = edcInCredit
        bill_lunch.tip_credit = tipCredit
        bill_lunch.wrong_credit = wrongCredit
        bill_lunch.detail_status = 1

        # Save the updated object
        bill_lunch.save()
        
        return redirect(reverse('lunch-input-detail', kwargs={'daily_report_id':daily_report_id}))

    return render(request,'keywordapp/lunch-input-quick.html',context={'date':date,'bill_lunch':bill_lunch})

def LunchInputDetail(request,daily_report_id):

    daily_object = get_object_or_404(DailyReportModel, id=daily_report_id)
    date = daily_object.date
    bill_lunch_id = daily_object.bill_lunch.id

    bill_lunch =  BillLunchModel.objects.get(id=bill_lunch_id)

    if request.method == 'POST':
        realBillOnlineCash = request.POST.get('real_bill_online_cash')
        realBillOnlineCashCount = request.POST.get('real_bill_online_cash_count')
        realBillOnlineCard = request.POST.get('real_bill_online_card')
        realBillOnlineCardCount = request.POST.get('real_bill_online_card_count')
        posTABillPhoneCash = request.POST.get('pos_ta_bill_phone_cash')
        posTABillPhoneCashCount = request.POST.get('pos_ta_bill_phone_cash_count')
        posTABillPhoneCard = request.POST.get('pos_ta_bill_phone_card')
        posTABillPhoneCardCount = request.POST.get('pos_ta_bill_phone_card_count')
        posInCash = request.POST.get('pos_in_bill_cash')
        posInCashCount = request.POST.get('pos_in_bill_cash_count')
        posInCard = request.POST.get('pos_in_bill_card')
        posInCardCount = request.POST.get('pos_in_bill_card_count')
        realBillTaPhoneDividePayCount = request.POST.get('real_bill_taphone_dividepay_count')
        realBillDineInDividePayCount = request.POST.get('real_bill_dinein_dividepay_count')
        realBillInCashCount = posInCashCount
        realBillInCash = posInCash
        realBillInCardCount = posInCardCount
        realBillInCard = posInCard
        realBillPhoneCashCount = posTABillPhoneCashCount
        realBillPhoneCash = posTABillPhoneCash
        realBillPhoneCardCount = posTABillPhoneCardCount
        realBillPhoneCard = posTABillPhoneCard


        edcInCredit = request.POST.get('edc_in_credit')

        bill_lunch =  get_object_or_404(BillLunchModel, id=bill_lunch_id)

        # Real Bill TA Phone
        bill_lunch.real_bill_phone_cash_count = realBillPhoneCashCount
        bill_lunch.real_bill_phone_cash = realBillPhoneCash
        bill_lunch.real_bill_phone_card_count = realBillPhoneCardCount
        bill_lunch.real_bill_phone_card = realBillPhoneCard
        bill_lunch.real_bill_taphone_dividepay_count = realBillTaPhoneDividePayCount
        bill_lunch.real_bill_dinein_dividepay_count = realBillDineInDividePayCount
        # Real Bill TA Online
        bill_lunch.real_bill_online_cash_count = realBillOnlineCashCount
        bill_lunch.real_bill_online_cash = realBillOnlineCash
        bill_lunch.real_bill_online_card_count = realBillOnlineCardCount
        bill_lunch.real_bill_online_card = realBillOnlineCard
        # Real Bill Dine in
        bill_lunch.real_bill_in_cash_count = realBillInCashCount
        bill_lunch.real_bill_in_cash = realBillInCash
        bill_lunch.real_bill_in_card_count = realBillInCardCount
        bill_lunch.real_bill_in_card = realBillInCard
        # POS TA Phone
        bill_lunch.pos_ta_bill_phone_cash = posTABillPhoneCash
        bill_lunch.pos_ta_bill_phone_cash_count = posTABillPhoneCashCount
        bill_lunch.pos_ta_bill_phone_card = posTABillPhoneCard
        bill_lunch.pos_ta_bill_phone_card_count = posTABillPhoneCardCount
        # POS Dine in
        bill_lunch.pos_in_bill_cash = posInCash
        bill_lunch.pos_in_bill_cash_count = posInCashCount
        bill_lunch.pos_in_bill_card = posInCard
        bill_lunch.pos_in_bill_card_count = posInCardCount
        # EDC Dine in
        bill_lunch.edc_in_credit = edcInCredit
        bill_lunch.detail_status = 1

        # Save the updated object
        bill_lunch.save()
        return redirect(reverse('lunch-report', kwargs={'daily_report_id':daily_report_id}))

    date = daily_object.date
    bill_lunch_id = daily_object.bill_lunch.id

    bill_lunch =  BillLunchModel.objects.get(id=bill_lunch_id)
    

    posTABillPhoneCard = bill_lunch.pos_ta_bill_phone_card
    posInCard = bill_lunch.pos_in_bill_card
    realBillOnlineCard = bill_lunch.real_bill_online_card
    edcInCredit = bill_lunch.edc_in_credit
    tipCredit = bill_lunch.tip_credit
    wrongCredit = bill_lunch.wrong_credit


    # Status
    sumBillPhoneCard = posTABillPhoneCard + posInCard + realBillOnlineCard
    addTipToSum = sumBillPhoneCard + tipCredit
    minusWrongCreditFromSumBillCard = addTipToSum - wrongCredit
    resultCheckEqual = "✅" if edcInCredit == minusWrongCreditFromSumBillCard else "❌"

    context = {
        'date': date,
        'bill_lunch': bill_lunch,
        'posInCard':posInCard,
        'addTipToSum':addTipToSum,
        'minusWrongCreditFromSumBillCard':minusWrongCreditFromSumBillCard,
        'posTABillPhoneCard':posTABillPhoneCard,
        'realBillOnlineCard':realBillOnlineCard,
        'sumBillPhoneCard':sumBillPhoneCard,
        'resultCheckEqual':resultCheckEqual,
        'edcInCredit':edcInCredit,
        'daily_report_id':daily_report_id,
    }
    return render(request,'keywordapp/lunch-input-detail.html',context)

def LunchReport(request,daily_report_id):

    daily_object = get_object_or_404(DailyReportModel, id=daily_report_id)
    # Retrieve other related models or fields if needed

    date = daily_object.date
    bill_lunch_id = daily_object.bill_lunch.id

    bill_lunch =  BillLunchModel.objects.get(id=bill_lunch_id)
    realBillPhoneCash = bill_lunch.real_bill_phone_cash
    realBillPhoneCashCount = bill_lunch.real_bill_phone_cash_count
    realBillPhoneCard = bill_lunch.real_bill_phone_card
    realBillPhoneCardCount = bill_lunch.real_bill_phone_card_count
    realBillOnlineCash = bill_lunch.real_bill_online_cash
    realBillOnlineCashCount = bill_lunch.real_bill_online_cash_count
    realBillOnlineCard = bill_lunch.real_bill_online_card
    realBillOnlineCardCount = bill_lunch.real_bill_online_card_count
    realBillTaPhoneDividePayCount = bill_lunch.real_bill_taphone_dividepay_count
    realBillDineInDividePayCount = bill_lunch.real_bill_dinein_dividepay_count
    realBillInCash = bill_lunch.real_bill_in_cash
    realBillInCashCount = bill_lunch.real_bill_in_cash_count
    realBillInCard = bill_lunch.real_bill_in_card
    realBillInCardCount = bill_lunch.real_bill_in_card_count
    edcInCredit = bill_lunch.edc_in_credit


    # Summary
    # Row 1 TA Online
    sumrealBillOnlineCount = realBillOnlineCashCount + realBillOnlineCardCount
    sumrealBillOnline = realBillOnlineCash + realBillOnlineCard
    # Row 2 TA Phone Lunch
    sumrealBillPhoneCount = realBillPhoneCashCount + realBillPhoneCardCount - realBillTaPhoneDividePayCount
    sumrealBillPhone = realBillPhoneCash + realBillPhoneCard
    # Row 3 Dine-in Lunch
    sumrealBillInCount = realBillInCashCount + realBillInCardCount - realBillDineInDividePayCount
    sumrealBillIn = realBillInCash + realBillInCard
    # Summary all Lunch
    totalBillLunch = sumrealBillPhone + sumrealBillIn + sumrealBillOnline
    context = {
        'date': date,
        'bill_lunch': bill_lunch,
        'daily_report_id': daily_report_id,

        # Row 1 Ta Online Lunch
        'realBillOnlineCash': realBillOnlineCash,
        'realBillOnlineCard': realBillOnlineCard,
        'sumrealBillOnlineCount': sumrealBillOnlineCount,
        'sumrealBillOnline': sumrealBillOnline,

        # Row 2 Ta Phone Lunch
        'realBillPhoneCash': realBillPhoneCash,
        'realBillPhoneCard': realBillPhoneCard,
        'sumrealBillPhoneCount': sumrealBillPhoneCount,
        'sumrealBillPhone': sumrealBillPhone,

        # Row 3 Dine-in Lunch
        'realBillInCash': realBillInCash,
        'realBillInCard': realBillInCard,
        'sumrealBillInCount': sumrealBillInCount,
        'sumrealBillIn': sumrealBillIn,
        
        # Row 4 Total
        'totalBillLunch': totalBillLunch,
        



        'edcInCredit':edcInCredit,
    }
    return render(request,'keywordapp/lunch-report.html',context)

#! DINNER

def DinnerInputQuick(request,daily_report_id):

    daily_object = get_object_or_404(DailyReportModel, id=daily_report_id)
    date = daily_object.date
    bill_dinner_id = daily_object.bill_dinner.id

    bill_dinner =  BillDinnerModel.objects.get(id=bill_dinner_id)

    if request.method == 'POST':
        realBillOnlineCard = request.POST.get('real_bill_online_card')
        posTABillPhoneCard = request.POST.get('pos_ta_bill_phone_card')
        realBillHomePhoneCard = request.POST.get('real_bill_home_phone_card')
        realBillHomeOnlineCard = request.POST.get('real_bill_home_online_card')
        posInCard = request.POST.get('pos_in_bill_card')
        edcInCredit = request.POST.get('edc_in_credit')
        tipCredit = request.POST.get('tip_credit')
        wrongCredit = request.POST.get('wrong_credit')
        edcHomeCredit = request.POST.get('edc_home_credit')

        bill_dinner =  get_object_or_404(BillDinnerModel, id=bill_dinner_id)
        bill_dinner.real_bill_online_card = realBillOnlineCard
        bill_dinner.pos_ta_bill_phone_card = posTABillPhoneCard
        bill_dinner.pos_in_bill_card = posInCard
        bill_dinner.real_bill_home_phone_card = realBillHomePhoneCard
        bill_dinner.real_bill_home_online_card = realBillHomeOnlineCard
        

        bill_dinner.wrong_credit = wrongCredit
        bill_dinner.tip_credit = tipCredit
        bill_dinner.edc_in_credit = edcInCredit
        bill_dinner.edc_home_credit = edcHomeCredit
        bill_dinner.detail_status = 1

        # Save the updated object
        bill_dinner.save()
        
        return redirect(reverse('dinner-input-detail', kwargs={'daily_report_id':daily_report_id}))

    return render(request,'keywordapp/dinner-input-quick.html',context={'date':date,'bill_dinner':bill_dinner})

def DinnerInputDetail(request, daily_report_id):

    daily_report = get_object_or_404(DailyReportModel, id=daily_report_id)
    date = daily_report.date
    bill_dinner_id = daily_report.bill_dinner.id
    bill_lunch_id = daily_report.bill_lunch.id

    bill_dinner =  BillDinnerModel.objects.get(id=bill_dinner_id)
    bill_lunch =  BillLunchModel.objects.get(id=bill_lunch_id)

    # Access the related DeliveryDetailModel instances using the foreign key relationship
    related_delivery_details = daily_report.bill_dinner.deliverydetailmodel_set.all()

    # Calculate the sum of the real_bill_home_oa_amount attribute for all DeliveryDetailModel instances
    realBillHomePhoneCashCount = sum(detail.real_bill_home_phone_cash_count for detail in related_delivery_details)
    realBillHomePhoneCash = sum(detail.real_bill_home_phone_cash for detail in related_delivery_details)
    realBillHomePhoneCardCount = sum(detail.real_bill_home_phone_card_count for detail in related_delivery_details)
    realBillHomePhoneCard = sum(detail.real_bill_home_phone_card for detail in related_delivery_details)
    realBillHomeOnlineCard = sum(detail.real_bill_home_online_card for detail in related_delivery_details)


    if request.method == 'POST':
        realBillOnlineCash = request.POST.get('real_bill_online_cash')
        realBillOnlineCashCount = request.POST.get('real_bill_online_cash_count')
        realBillOnlineCard = request.POST.get('real_bill_online_card')
        realBillOnlineCardCount = request.POST.get('real_bill_online_card_count')
        posTABillPhoneCash = request.POST.get('pos_ta_bill_phone_cash')
        posTABillPhoneCashCount = request.POST.get('pos_ta_bill_phone_cash_count')
        posTABillPhoneCard = request.POST.get('pos_ta_bill_phone_card')
        posTABillPhoneCardCount = request.POST.get('pos_ta_bill_phone_card_count')
        posInCash = request.POST.get('pos_in_bill_cash')
        posInCashCount = request.POST.get('pos_in_bill_cash_count')
        posInCard = request.POST.get('pos_in_bill_card')
        posInCardCount = request.POST.get('pos_in_bill_card_count')
        realBillTaPhoneDividePayCount = request.POST.get('real_bill_taphone_dividepay_count')
        realBillDineInDividePayCount = request.POST.get('real_bill_dinein_dividepay_count')
        realBillInCashCount = posInCashCount
        realBillInCash = posInCash
        realBillInCardCount = posInCardCount
        realBillInCard = posInCard

        wrongCredit = request.POST.get('wrong_credit')
        tipCredit = request.POST.get('tip_credit')
        edcInCredit = request.POST.get('edc_in_credit')


        # Calculation 
        realBillPhoneCashCount = int(posTABillPhoneCashCount) - int(realBillHomePhoneCashCount)
        realBillPhoneCash = Decimal(posTABillPhoneCash) - Decimal(realBillHomePhoneCash)
        realBillPhoneCardCount = int(posTABillPhoneCardCount) - int(realBillHomePhoneCardCount)
        realBillPhoneCard = Decimal(posTABillPhoneCard) - Decimal(realBillHomePhoneCard)


        bill_dinner =  get_object_or_404(BillDinnerModel, id=bill_dinner_id)



        # Real Bill TA Phone
        bill_dinner.real_bill_phone_cash_count = realBillPhoneCashCount
        bill_dinner.real_bill_phone_cash = realBillPhoneCash
        bill_dinner.real_bill_phone_card_count = realBillPhoneCardCount
        bill_dinner.real_bill_phone_card = realBillPhoneCard
        bill_dinner.real_bill_taphone_dividepay_count = realBillTaPhoneDividePayCount
        bill_dinner.real_bill_dinein_dividepay_count = realBillDineInDividePayCount
        # Real Bill TA Online
        bill_dinner.real_bill_online_cash_count = realBillOnlineCashCount
        bill_dinner.real_bill_online_cash = realBillOnlineCash
        bill_dinner.real_bill_online_card_count = realBillOnlineCardCount
        bill_dinner.real_bill_online_card = realBillOnlineCard
        # Real Bill Dine in
        bill_dinner.real_bill_in_cash_count = realBillInCashCount
        bill_dinner.real_bill_in_cash = realBillInCash
        bill_dinner.real_bill_in_card_count = realBillInCardCount
        bill_dinner.real_bill_in_card = realBillInCard
        # POS TA Phone
        bill_dinner.pos_ta_bill_phone_cash = posTABillPhoneCash
        bill_dinner.pos_ta_bill_phone_cash_count = posTABillPhoneCashCount
        bill_dinner.pos_ta_bill_phone_card = posTABillPhoneCard
        bill_dinner.pos_ta_bill_phone_card_count = posTABillPhoneCardCount
        # POS Dine in
        bill_dinner.pos_in_bill_cash = posInCash
        bill_dinner.pos_in_bill_cash_count = posInCashCount
        bill_dinner.pos_in_bill_card = posInCard
        bill_dinner.pos_in_bill_card_count = posInCardCount
        # EDC Dine in
        bill_dinner.tip_credit = tipCredit
        bill_dinner.wrong_credit = wrongCredit
        bill_dinner.edc_in_credit = edcInCredit
        bill_dinner.detail_status = 1

        # Save the updated object
        bill_dinner.save()
        return redirect(reverse('dinner-report', kwargs={'daily_report_id': daily_report_id}))


    bill_dinner =  BillDinnerModel.objects.get(id=bill_dinner_id)
    bill_lunch =  BillLunchModel.objects.get(id=bill_lunch_id)

    # get data for general data LUNCH
    edcInCreditLunch = bill_lunch.edc_in_credit

    # get data for general data DINNER
    posTABillPhoneCard = bill_dinner.pos_ta_bill_phone_card
    posInCard = bill_dinner.pos_in_bill_card
    realBillOnlineCard = bill_dinner.real_bill_online_card
    edcInCredit = bill_dinner.edc_in_credit
    tipCredit = bill_dinner.tip_credit
    wrongCredit = bill_dinner.wrong_credit

    # Calculate
    # Minus Home Phone Out From POS TA
    minusHomePhoneOutFromPosTa = posTABillPhoneCard - realBillHomePhoneCard
    # Sum 
    sumBillCardForEdcDineIn = minusHomePhoneOutFromPosTa + posInCard + realBillOnlineCard + tipCredit
    minusWrongCreditFromSumBillCard = sumBillCardForEdcDineIn - wrongCredit
    sumBillHomeCard = realBillHomePhoneCard + realBillHomeOnlineCard
    # Dinner EDC minus Lunch EDC
    edcInCreditResult = edcInCredit - edcInCreditLunch
    # Compare
    resultCheckEqual1 = "✅" if minusWrongCreditFromSumBillCard == edcInCreditResult else "❌"
    # resultCheckEqual2 = "✅" if sumBillHomeCard == edcHomeCredit else "❌"

    context = {
        'date': date,
        'bill_dinner': bill_dinner,
        'posInCard': posInCard,
        'posTABillPhoneCard': posTABillPhoneCard,
        'realBillOnlineCard': realBillOnlineCard,
        'sumBillCardForEdcDineIn': sumBillCardForEdcDineIn,
        'minusHomePhoneOutFromPosTa': minusHomePhoneOutFromPosTa,
        'minusWrongCreditFromSumBillCard': minusWrongCreditFromSumBillCard,
        'resultCheckEqual1': resultCheckEqual1,
        'edcInCredit': edcInCredit,
        'edcInCreditLunch': edcInCreditLunch,
        'edcInCreditResult': edcInCreditResult,
        # Home 
        'realBillHomePhoneCard': realBillHomePhoneCard,
        'realBillHomeOnlineCard': realBillHomeOnlineCard,
        'sumBillHomeCard': sumBillHomeCard,
        'daily_report_id': daily_report_id,
    }
    return render(request, 'keywordapp/dinner-input-detail.html', context)

def DinnerReport(request,daily_report_id):

    daily_report = get_object_or_404(DailyReportModel, id=daily_report_id)
    # Retrieve other related models or fields if needed

    date = daily_report.date
    bill_lunch_id = daily_report.bill_lunch.id
    bill_dinner_id = daily_report.bill_dinner.id

    #* Lunch Data
    bill_lunch =  BillLunchModel.objects.get(id=bill_lunch_id)
    realBillPhoneCashLunch = bill_lunch.real_bill_phone_cash
    realBillPhoneCashCountLunch = bill_lunch.real_bill_phone_cash_count
    realBillPhoneCardLunch = bill_lunch.real_bill_phone_card
    realBillPhoneCardCountLunch = bill_lunch.real_bill_phone_card_count
    realBillOnlineCashLunch = bill_lunch.real_bill_online_cash
    realBillOnlineCashCountLunch = bill_lunch.real_bill_online_cash_count
    realBillOnlineCardLunch = bill_lunch.real_bill_online_card
    realBillOnlineCardCountLunch = bill_lunch.real_bill_online_card_count
    realBillTaPhoneDividePayCountLunch = bill_lunch.real_bill_taphone_dividepay_count
    realBillDineInDividePayCountLunch = bill_lunch.real_bill_dinein_dividepay_count
    realBillInCashLunch = bill_lunch.real_bill_in_cash
    realBillInCashCountLunch = bill_lunch.real_bill_in_cash_count
    realBillInCardLunch = bill_lunch.real_bill_in_card
    realBillInCardCountLunch = bill_lunch.real_bill_in_card_count
    tipLunch = bill_lunch.tip_credit
    wrongCreditLunch = bill_lunch.wrong_credit

    #* Dinner Data
    bill_dinner =  BillDinnerModel.objects.get(id=bill_dinner_id)
    realBillPhoneCashDinner = bill_dinner.real_bill_phone_cash
    realBillPhoneCashCountDinner = bill_dinner.real_bill_phone_cash_count
    realBillPhoneCardDinner = bill_dinner.real_bill_phone_card
    realBillPhoneCardCountDinner = bill_dinner.real_bill_phone_card_count
    realBillOnlineCashDinner = bill_dinner.real_bill_online_cash
    realBillOnlineCashCountDinner = bill_dinner.real_bill_online_cash_count
    realBillOnlineCardDinner = bill_dinner.real_bill_online_card
    realBillOnlineCardCountDinner = bill_dinner.real_bill_online_card_count
    realBillTaPhoneDividePayCountDinner = bill_dinner.real_bill_taphone_dividepay_count
    realBillDineInDividePayCountDinner = bill_dinner.real_bill_dinein_dividepay_count
    realBillInCashDinner = bill_dinner.real_bill_in_cash
    realBillInCashCountDinner = bill_dinner.real_bill_in_cash_count
    realBillInCardDinner = bill_dinner.real_bill_in_card
    realBillInCardCountDinner = bill_dinner.real_bill_in_card_count
    tipDinner = bill_dinner.tip_credit
    wrongCreditDinner = bill_dinner.wrong_credit

    #* Delivery Section
    # Access the related DeliveryDetailModel instances using the foreign key relationship
    related_delivery_details = daily_report.bill_dinner.deliverydetailmodel_set.all()
    
    # Summarize the number of delivery man
    for detail in related_delivery_details:
            detail.sum_commission = int(detail.wage_per_home * (detail.real_bill_home_phone_cash_count + detail.real_bill_home_phone_card_count + detail.real_bill_home_online_cash_count + detail.real_bill_home_online_card_count))
            detail.home_count = detail.real_bill_home_phone_cash_count + detail.real_bill_home_phone_card_count + detail.real_bill_home_online_cash_count + detail.real_bill_home_online_card_count
            detail.sum_commission_and_oa = int((detail.real_bill_home_oa_count * detail.real_bill_home_oa_amount) + detail.sum_commission)
            if detail.real_bill_home_oa_count > 0:
                detail.show_oa_count = " + "+str(detail.real_bill_home_oa_count)+" OA"
            if detail.real_bill_home_oa_amount > 0:
                detail.show_oa_amount = " + "+str(int(detail.real_bill_home_oa_amount))
        
    totalSumCommissionAndOa = sum(detail.sum_commission_and_oa for detail in related_delivery_details)


    # sum all without separating delivery man
    realBillHomePhoneCashCountDinner = sum(detail.real_bill_home_phone_cash_count for detail in related_delivery_details)
    realBillHomePhoneCashDinner = sum(detail.real_bill_home_phone_cash for detail in related_delivery_details)
    realBillHomePhoneCardCountDinner = sum(detail.real_bill_home_phone_card_count for detail in related_delivery_details)
    realBillHomePhoneCardDinner = sum(detail.real_bill_home_phone_card for detail in related_delivery_details)
    realBillHomeOnlineCashCountDinner = sum(detail.real_bill_home_online_cash_count for detail in related_delivery_details)
    realBillHomeOnlineCashDinner = sum(detail.real_bill_home_online_cash for detail in related_delivery_details)
    realBillHomeOnlineCardCountDinner = sum(detail.real_bill_home_online_card_count for detail in related_delivery_details)
    realBillHomeOnlineCardDinner = sum(detail.real_bill_home_online_card for detail in related_delivery_details)

    #? Summary
    #* Report Section
    # Row 1
    totalBillLunch = realBillPhoneCashLunch + realBillPhoneCardLunch + realBillInCashLunch + realBillInCardLunch + realBillOnlineCashLunch + realBillOnlineCardLunch
    # Row 10
    sumTotal = realBillOnlineCashLunch + realBillOnlineCardLunch + realBillPhoneCashLunch + realBillPhoneCardLunch + realBillInCashLunch + realBillInCardLunch + realBillHomePhoneCashDinner + realBillHomePhoneCardDinner + realBillHomeOnlineCashDinner + realBillHomeOnlineCardDinner + realBillPhoneCashDinner + realBillPhoneCardDinner + realBillOnlineCashDinner + realBillOnlineCardDinner + realBillInCashDinner + realBillInCardDinner
    # Row 4
    totalBillDinner = intcomma(sumTotal - totalBillLunch)
    # Row 4
    sumrealBillHomePhoneCountDinner = realBillHomePhoneCashCountDinner + realBillHomePhoneCardCountDinner
    # Row 5
    sumrealBillHomeOnlineCountDinner = realBillHomeOnlineCashCountDinner + realBillHomeOnlineCardCountDinner
    # Row 7
    sumrealBillOnlineCountDinner = realBillOnlineCashCountDinner + realBillOnlineCardCountDinner
    # Row 10 Column 4
    sumCash = intcomma(realBillOnlineCashLunch + realBillPhoneCashLunch + realBillInCashLunch + realBillHomePhoneCashDinner + realBillHomeOnlineCashDinner + realBillPhoneCashDinner + realBillOnlineCashDinner + realBillInCashDinner)
    # Row 10 Column 5
    sumCard = intcomma(realBillOnlineCardLunch + realBillPhoneCardLunch + realBillInCardLunch + realBillHomePhoneCardDinner + realBillHomeOnlineCardDinner + realBillPhoneCardDinner + realBillOnlineCardDinner + realBillInCardDinner)
    
    #* Delivery section
    # Sum all count both phone and online and
    sumrealBillHomeCountDinner = sumrealBillHomePhoneCountDinner + sumrealBillHomeOnlineCountDinner

    #* Other section
    sumTip = intcomma(tipLunch + tipDinner)
    sumWrongCredit = intcomma(wrongCreditLunch + wrongCreditDinner)
    totalOnlineCount = intcomma(realBillOnlineCardCountLunch + realBillOnlineCashCountLunch + realBillOnlineCashCountDinner + realBillOnlineCardCountDinner + realBillHomeOnlineCashCountDinner + realBillHomeOnlineCardCountDinner)
    totalOnlineAmount = intcomma(realBillOnlineCardLunch + realBillOnlineCashLunch + realBillOnlineCashDinner + realBillOnlineCardDinner + realBillHomeOnlineCashDinner + realBillHomeOnlineCardDinner)



    context = {
        'date': date,
        'daily_report_id': daily_report_id,
        #! Lunch
        # Row 1 Ta Online Lunch
        'sumrealBillOnlineCount': realBillOnlineCashCountLunch + realBillOnlineCardCountLunch,
        'sumrealBillOnline': intcomma(realBillOnlineCashLunch + realBillOnlineCardLunch),
        'realBillOnlineCashLunch': realBillOnlineCashLunch,
        'realBillOnlineCardLunch': realBillOnlineCardLunch,
        # Row 2 Ta Phone Lunch
        'sumrealBillPhoneCount': realBillPhoneCashCountLunch + realBillPhoneCardCountLunch - realBillTaPhoneDividePayCountLunch,
        'sumrealBillPhone': intcomma(realBillPhoneCashLunch + realBillPhoneCardLunch),
        'realBillPhoneCashLunch': realBillPhoneCashLunch,
        'realBillPhoneCardLunch': realBillPhoneCardLunch,
        # Row 3 Dine-in Lunch
        'sumrealBillInCount': realBillInCashCountLunch + realBillInCardCountLunch - realBillDineInDividePayCountLunch,
        'sumrealBillIn': intcomma(realBillInCashLunch + realBillInCardLunch),
        'realBillInCashLunch': realBillInCashLunch,
        'realBillInCardLunch': realBillInCardLunch,
        #! Dinner
        # Row 4 Home Phone
        'realBillHomePhoneCashDinner': realBillHomePhoneCashDinner,
        'realBillHomePhoneCardDinner': realBillHomePhoneCardDinner,
        'sumrealBillHomePhoneCountDinner': sumrealBillHomePhoneCountDinner,
        'sumrealBillHomePhoneDinner': intcomma(realBillHomePhoneCashDinner + realBillHomePhoneCardDinner),
        # Row 5 Home Online
        'realBillHomeOnlineCashDinner': realBillHomeOnlineCashDinner,
        'realBillHomeOnlineCardDinner': realBillHomeOnlineCardDinner,
        'sumrealBillHomeOnlineCountDinner': sumrealBillHomeOnlineCountDinner,
        'sumrealBillHomeOnlineDinner': intcomma(realBillHomeOnlineCashDinner + realBillHomeOnlineCardDinner),
        # Row 6 T/A Phone Dinner
        'sumrealBillPhoneCountDinner': realBillPhoneCashCountDinner + realBillPhoneCardCountDinner - realBillTaPhoneDividePayCountDinner,
        'sumrealBillPhoneDinner': intcomma(realBillPhoneCashDinner + realBillPhoneCardDinner),
        'realBillPhoneCashDinner': realBillPhoneCashDinner,
        'realBillPhoneCardDinner': realBillPhoneCardDinner,
        # Row 7 T/A Online Dinner
        'sumrealBillOnlineCountDinner': sumrealBillOnlineCountDinner,
        'sumrealBillOnlineDinner': intcomma(realBillOnlineCashDinner + realBillOnlineCardDinner),
        'realBillOnlineCashDinner': realBillOnlineCashDinner,
        'realBillOnlineCardDinner': realBillOnlineCardDinner,
        # Row 8 Dine-in Dinner
        'sumrealBillInCountDinner': realBillInCashCountDinner + realBillInCardCountDinner - realBillDineInDividePayCountDinner,
        'sumrealBillInDinner': intcomma(realBillInCashDinner + realBillInCardDinner),
        'realBillInCashDinner': realBillInCashDinner,
        'realBillInCardDinner': realBillInCardDinner,
        #! Total
        'totalBillLunch': totalBillLunch,
        'totalBillDinner': totalBillDinner,
        'sumTotal': sumTotal,
        'sumCash': sumCash,
        'sumCard': sumCard,
        'sumTip': sumTip,
        'sumWrongCredit': sumWrongCredit,
        'totalOnlineAmount': totalOnlineAmount,
        'totalOnlineCount': totalOnlineCount,

        #! Home section
        'related_delivery_details': related_delivery_details,
        'sumrealBillHomeCountDinner': sumrealBillHomeCountDinner,
        'totalSumCommissionAndOa': totalSumCommissionAndOa,
        
    }
    return render(request,'keywordapp/dinner-report.html',context)

def HomeList(request,daily_report_id):

    daily_report = get_object_or_404(DailyReportModel, id=daily_report_id)
    date = daily_report.date

    # You can also access the related DeliveryDetailModel instances from a DailyReportModel instance
    related_delivery_details = daily_report.bill_dinner.deliverydetailmodel_set.all()
    for detail in related_delivery_details:
        detail.sum_commission = detail.wage_per_home * (detail.real_bill_home_phone_cash_count + detail.real_bill_home_phone_card_count + detail.real_bill_home_online_cash_count + detail.real_bill_home_online_card_count)
        detail.home_count = detail.real_bill_home_phone_cash_count + detail.real_bill_home_phone_card_count + detail.real_bill_home_online_cash_count + detail.real_bill_home_online_card_count
        detail.sum_commission_and_oa = (detail.real_bill_home_oa_count * detail.real_bill_home_oa_amount) + detail.sum_commission

    context ={
        'date': date,
        'daily_report_id': daily_report_id,
        'related_delivery_details': related_delivery_details,
    }
    return render(request,'keywordapp/home-list.html',context)

def HomeInputQuick(request,daily_report_id,delivery_id):

    daily_object = get_object_or_404(DailyReportModel, id=daily_report_id)
    date = daily_object.date
    bill_dinner = daily_object.bill_dinner
    if delivery_id == 0:
        newDeliveryMan = DeliveryDetailModel.objects.create(bill_dinner=bill_dinner)
        newDeliveryManId = newDeliveryMan.id
        return redirect(reverse('home-input-quick', kwargs={'daily_report_id':daily_report_id,'delivery_id':newDeliveryManId}))

    if request.method == 'POST':
        # Home
        realBillHomePhoneCashCount = request.POST.get('real_bill_home_phone_cash_count')
        realBillHomePhoneCash = request.POST.get('real_bill_home_phone_cash')
        realBillHomePhoneCardCount = request.POST.get('real_bill_home_phone_card_count')
        realBillHomePhoneCard = request.POST.get('real_bill_home_phone_card')
        realBillHomeOnlineCashCount = request.POST.get('real_bill_home_online_cash_count')
        realBillHomeOnlineCash = request.POST.get('real_bill_home_online_cash')
        realBillHomeOnlineCardCount = request.POST.get('real_bill_home_online_card_count')
        realBillHomeOnlineCard = request.POST.get('real_bill_home_online_card')

        realBillHomeOaCount = request.POST.get('real_bill_home_oa_count')
        realBillHomeOaAmount = request.POST.get('real_bill_home_oa_amount')
        deliveryName = request.POST.get('delivery_name')
        wagePerHour = request.POST.get('wage_per_home')

        delivery_detail =  get_object_or_404(DeliveryDetailModel, id=delivery_id)

        # Home  Phone
        delivery_detail.real_bill_home_phone_cash_count = realBillHomePhoneCashCount
        delivery_detail.real_bill_home_phone_cash = realBillHomePhoneCash
        delivery_detail.real_bill_home_phone_card_count = realBillHomePhoneCardCount
        delivery_detail.real_bill_home_phone_card = realBillHomePhoneCard
        # Home  Online
        delivery_detail.real_bill_home_online_cash_count = realBillHomeOnlineCashCount
        delivery_detail.real_bill_home_online_cash = realBillHomeOnlineCash
        delivery_detail.real_bill_home_online_card_count = realBillHomeOnlineCardCount
        delivery_detail.real_bill_home_online_card = realBillHomeOnlineCard
        # OA
        delivery_detail.real_bill_home_oa_count = realBillHomeOaCount
        delivery_detail.real_bill_home_oa_amount = realBillHomeOaAmount
        # Delivery man
        delivery_detail.delivery_name = deliveryName
        delivery_detail.wage_per_home = wagePerHour


        delivery_detail.save()

        return redirect(reverse('home-input-detail', kwargs={'daily_report_id':daily_report_id,'delivery_id':delivery_id}))


    delivery_detail =  DeliveryDetailModel.objects.get(id=delivery_id)


    context ={
        'date': date,
        'daily_report_id': daily_report_id,
        'delivery_detail': delivery_detail,
    }
    return render(request,'keywordapp/home-input-quick.html',context)

def HomeInputDetail(request,daily_report_id,delivery_id):
    
    daily_object = get_object_or_404(DailyReportModel, id=daily_report_id)
    date = daily_object.date
    delivery_detail =  DeliveryDetailModel.objects.get(id=delivery_id)
    
    # Summary
    sumHomePhoneCount = delivery_detail.real_bill_home_phone_cash_count + delivery_detail.real_bill_home_phone_card_count
    sumHomeOnlineCount = delivery_detail.real_bill_home_online_cash_count + delivery_detail.real_bill_home_online_card_count
    sumHomeCount = delivery_detail.real_bill_home_phone_cash_count + delivery_detail.real_bill_home_phone_card_count + delivery_detail.real_bill_home_online_cash_count  + delivery_detail.real_bill_home_online_card_count

    #Calculation
    sumHomeCommission = sumHomeCount * delivery_detail.wage_per_home
    sumHomeCommissionAndOa = sumHomeCommission + (delivery_detail.real_bill_home_oa_amount * delivery_detail.real_bill_home_oa_count)

    context ={
        'date': date,
        'delivery_detail': delivery_detail,
        'daily_report_id': daily_report_id,
        'sumHomeCount': sumHomeCount,
        'sumHomePhoneCount': sumHomePhoneCount,
        'sumHomeOnlineCount': sumHomeOnlineCount,
        'sumHomeCommission': sumHomeCommission,
        'sumHomeCommissionAndOa': sumHomeCommissionAndOa,
    }
    return render(request,'keywordapp/home-input-detail.html',context)

def HomeResult(request):
    return render(request,'keywordapp/home-result.html')
