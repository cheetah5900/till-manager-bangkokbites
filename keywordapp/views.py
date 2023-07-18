
# =============================== FOR PAGE KEYWORD MANAGER ===============================
# =============================== FOR PAGE KEYWORD MANAGER ===============================
# =============================== FOR PAGE KEYWORD MANAGER ===============================

from django.shortcuts import render, redirect,get_object_or_404
from django.urls import reverse
from django.utils import timezone


from datetime import date,timedelta,datetime

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
            real_bill = RealBillModel.objects.create()
            pos_detail = PosDetailModel.objects.create()
            edc_detail = EdcDetailModel.objects.create()
            delivery_detail = DeliveryDetailModel.objects.create()

            # get last id
            real_bill_id = real_bill.id
            pos_detail_id = pos_detail.id
            edc_detail_id = edc_detail.id
            delivery_detail_id = delivery_detail.id

            # create daily report
            daily_report = DailyReportModel.objects.create(
                date=choose_date,
                real_bill_id=real_bill_id,
                pos_detail_id=pos_detail_id,
                edc_detail_id=edc_detail_id,
                delivery_detail_id=delivery_detail_id
            )
            
        if mode == 'lunch':
            return redirect(reverse('lunch-input-quick', kwargs={'daily_report_id': daily_report.id}))


    return render(request, 'keywordapp/index.html', context)


def HomeInput(request):

    return render(request,'keywordapp/home-input.html')

def LunchInputQuick(request,daily_report_id):

    daily_object = get_object_or_404(DailyReportModel, id=daily_report_id)
    date = daily_object.date
    real_bill_id = daily_object.real_bill.id

    real_bill = RealBillModel.objects.get(id=real_bill_id)

    if request.method == 'POST':
        realBillOnlineCard = request.POST.get('real_bill_online_card')
        posTABillPhoneCard = request.POST.get('pos_ta_bill_phone_card')
        posInCard = request.POST.get('pos_in_bill_card')
        edcInCredit = request.POST.get('edc_in_credit')

        real_bill = get_object_or_404(RealBillModel, id=real_bill_id)
        real_bill.real_bill_online_card = realBillOnlineCard
        real_bill.pos_ta_bill_phone_card = posTABillPhoneCard
        real_bill.pos_in_bill_card = posInCard
        real_bill.edc_in_credit = edcInCredit
        real_bill.detail_status = 1

        # Save the updated object
        real_bill.save()
        
        return redirect(reverse('lunch-input', kwargs={'daily_report_id':daily_report_id}))

    return render(request,'keywordapp/lunch-input-quick.html',context={'date':date,'data':real_bill})

def LunchInputDetail(request,daily_report_id):

    daily_object = get_object_or_404(DailyReportModel, id=daily_report_id)
    date = daily_object.date
    real_bill_id = daily_object.real_bill.id
    edc_detail_id = daily_object.edc_detail.id
    pos_detail_id = daily_object.pos_detail.id
    delivery_detail_id = daily_object.delivery_detail.id

    real_bill = RealBillModel.objects.get(id=real_bill_id)

    if request.method == 'POST':
        realBillPhoneCash = request.POST.get('real_bill_phone_cash')
        realBillPhoneCashCount = request.POST.get('real_bill_phone_cash_count')
        realBillPhoneCard = request.POST.get('real_bill_phone_card')
        realBillPhoneCardCount = request.POST.get('real_bill_phone_card_count')
        realBillOnlineCash = request.POST.get('real_bill_online_cash')
        realBillOnlineCashCount = request.POST.get('real_bill_online_cash_count')
        realBillOnlineCard = request.POST.get('real_bill_online_card')
        realBillOnlineCardCount = request.POST.get('real_bill_online_card_count')
        realBillInCash = request.POST.get('real_bill_in_cash')
        realBillInCashCount = request.POST.get('real_bill_in_cash_count')
        realBillInCard = request.POST.get('real_bill_in_card')
        realBillInCardCount = request.POST.get('real_bill_in_card_count')
        posTABillPhoneCash = request.POST.get('pos_ta_bill_phone_cash')
        posTABillPhoneCashCount = request.POST.get('pos_ta_bill_phone_cash_count')
        posTABillPhoneCard = request.POST.get('pos_ta_bill_phone_card')
        posTABillPhoneCardCount = request.POST.get('pos_ta_bill_phone_card_count')
        posInCash = request.POST.get('pos_in_bill_cash')
        posInCashCount = request.POST.get('pos_in_bill_cash_count')
        posInCard = request.POST.get('pos_in_bill_card')
        posInCardCount = request.POST.get('pos_in_bill_card_count')
        copyData = request.POST.get('copy_data')

        edcInCredit = request.POST.get('edc_in_credit')

        real_bill = get_object_or_404(RealBillModel, id=real_bill_id)
        # Update the attributes of the existing object
        if copyData == "on":
            realBillPhoneCashCount = posTABillPhoneCashCount
            realBillPhoneCash = posTABillPhoneCash
            realBillPhoneCardCount = posTABillPhoneCardCount
            realBillPhoneCard = posTABillPhoneCard
            realBillInCashCount = posInCashCount
            realBillInCash = posInCash
            realBillInCardCount = posInCardCount
            realBillInCard = posInCard

        # Real Bill TA Phone
        real_bill.real_bill_phone_cash_count = realBillPhoneCashCount
        real_bill.real_bill_phone_cash = realBillPhoneCash
        real_bill.real_bill_phone_card_count = realBillPhoneCardCount
        real_bill.real_bill_phone_card = realBillPhoneCard
        # Real Bill TA Online
        real_bill.real_bill_online_cash_count = realBillOnlineCashCount
        real_bill.real_bill_online_cash = realBillOnlineCash
        real_bill.real_bill_online_card_count = realBillOnlineCardCount
        real_bill.real_bill_online_card = realBillOnlineCard
        # Real Bill Dine in
        real_bill.real_bill_in_cash_count = realBillInCashCount
        real_bill.real_bill_in_cash = realBillInCash
        real_bill.real_bill_in_card_count = realBillInCardCount
        real_bill.real_bill_in_card = realBillInCard
        # POS TA Phone
        real_bill.pos_ta_bill_phone_cash = posTABillPhoneCash
        real_bill.pos_ta_bill_phone_cash_count = posTABillPhoneCashCount
        real_bill.pos_ta_bill_phone_card = posTABillPhoneCard
        real_bill.pos_ta_bill_phone_card_count = posTABillPhoneCardCount
        # POS Dine in
        real_bill.pos_in_bill_cash = posInCash
        real_bill.pos_in_bill_cash_count = posInCashCount
        real_bill.pos_in_bill_card = posInCard
        real_bill.pos_in_bill_card_count = posInCardCount
        # EDC Dine in
        real_bill.edc_in_credit = edcInCredit
        real_bill.detail_status = 1

        # Save the updated object
        real_bill.save()
        if 'updateandcalculate' in request.POST:
            return redirect(reverse('lunch-result', kwargs={'daily_report_id':daily_report_id}))

    date = daily_object.date
    real_bill_id = daily_object.real_bill.id

    real_bill = RealBillModel.objects.get(id=real_bill_id)
    

    posTABillPhoneCard = real_bill.pos_ta_bill_phone_card
    posInCard = real_bill.pos_in_bill_card
    realBillOnlineCard = real_bill.real_bill_online_card
    edcInCredit = real_bill.edc_in_credit


    # Status
    sumBillPhoneCard = posTABillPhoneCard + posInCard + realBillOnlineCard
    resultCheckEqual = "✅" if edcInCredit == sumBillPhoneCard else "❌"

    context = {
        'date': date,
        'real_bill': real_bill,
        'posInCard':posInCard,
        'posTABillPhoneCard':posTABillPhoneCard,
        'realBillOnlineCard':realBillOnlineCard,
        'sumBillPhoneCard':sumBillPhoneCard,
        'resultCheckEqual':resultCheckEqual,
        'edcInCredit':edcInCredit,
        'daily_report_id':daily_report_id,
    }
    return render(request,'keywordapp/lunch-input-detail.html',context)


def LunchResult(request,daily_report_id):

    daily_object = get_object_or_404(DailyReportModel, id=daily_report_id)
    # Retrieve other related models or fields if needed

    date = daily_object.date
    real_bill_id = daily_object.real_bill.id
    edc_detail_id = daily_object.edc_detail.id
    pos_detail_id = daily_object.pos_detail.id
    delivery_detail_id = daily_object.delivery_detail.id

    real_bill = RealBillModel.objects.get(id=real_bill_id)
    realBillPhoneCash = real_bill.real_bill_phone_cash
    realBillPhoneCashCount = real_bill.real_bill_phone_cash_count
    realBillPhoneCard = real_bill.real_bill_phone_card
    realBillPhoneCardCount = real_bill.real_bill_phone_card_count
    realBillOnlineCash = real_bill.real_bill_online_cash
    realBillOnlineCashCount = real_bill.real_bill_online_cash_count
    realBillOnlineCard = real_bill.real_bill_online_card
    realBillOnlineCardCount = real_bill.real_bill_online_card_count
    realBillInCash = real_bill.real_bill_in_cash
    realBillInCashCount = real_bill.real_bill_in_cash_count
    realBillInCard = real_bill.real_bill_in_card
    realBillInCardCount = real_bill.real_bill_in_card_count
    posTABillPhoneCash = real_bill.pos_ta_bill_phone_cash
    posTABillPhoneCashCount = real_bill.pos_ta_bill_phone_cash_count
    posTABillPhoneCard = real_bill.pos_ta_bill_phone_card
    posTABillPhoneCardCount = real_bill.pos_ta_bill_phone_card_count
    posInCash = real_bill.pos_in_bill_cash
    posInCashCount = real_bill.pos_in_bill_cash_count
    posInCard = real_bill.pos_in_bill_card
    posInCardCount = real_bill.pos_in_bill_card_count
    edcInCredit = real_bill.edc_in_credit
    detailStatus = real_bill.detail_status

    # Status
    # Table 1 TA Phone
    resultPhoneCashCount = "✅" if realBillPhoneCashCount == posTABillPhoneCashCount else "❌"
    resultPhoneCardCount = "✅" if realBillPhoneCardCount == posTABillPhoneCardCount else "❌"
    resultPhoneCash = "✅" if realBillPhoneCash == posTABillPhoneCash else "❌"
    resultPhoneCard = "✅" if realBillPhoneCard == posTABillPhoneCard else "❌"

    # Table 2 Dine-in
    resultInCashCount = "✅" if realBillInCashCount == posInCashCount else "❌"
    resultInCardCount = "✅" if realBillInCardCount == posInCardCount else "❌"
    resultInCash = "✅" if realBillInCash == posInCash else "❌"
    resultInCard = "✅" if realBillInCard == posInCard else "❌"

    # Summary
    # Table 1 TA Phone
    sumrealBillPhoneCount = realBillPhoneCashCount + realBillPhoneCardCount
    sumrealBillPhone = realBillPhoneCash + realBillPhoneCard
    sumposTABillPhoneCount = posTABillPhoneCashCount + posTABillPhoneCardCount
    sumposTABillPhone = posTABillPhoneCash + posTABillPhoneCard
    # Table 2 Dine-in
    sumrealBillInCount = realBillInCashCount + realBillInCardCount
    sumrealBillIn = realBillInCash + realBillInCard
    sumposInCount = posInCashCount + posInCardCount
    sumposIn = posInCash + posInCard
    # Table 3 TA Online
    sumrealBillOnlineCount = realBillOnlineCashCount + realBillOnlineCardCount
    sumrealBillOnline = realBillOnlineCash + realBillOnlineCard

    # Check equality 
    # TABLE 1 TA Phone
    resultPhoneCount = "✅" if sumrealBillPhoneCount == sumposTABillPhoneCount else "❌"
    resultPhone = "✅" if sumrealBillPhone == sumposTABillPhone else "❌"
    # TABLE 2 Dine-in
    resultInCount = "✅" if sumrealBillInCount == sumposInCount else "❌"
    resultIn = "✅" if sumrealBillIn == sumposIn else "❌"

    # Status of each result table
    # Table 1 Ta Phone
    if resultPhoneCashCount == "✅" and resultPhoneCardCount == "✅" and resultPhoneCash == "✅" and resultPhoneCard == "✅" and resultPhoneCount == "✅" and resultPhone == "✅":
        statusTableTaPhone = "✅"
    else:
        statusTableTaPhone = "❌"
    # Table 2 Dine-in
    if resultInCashCount == "✅" and resultInCardCount == "✅" and resultInCash == "✅" and resultInCard == "✅" and resultInCount == "✅" and resultIn == "✅":
        statusTableIn = "✅"
    else:
        statusTableIn = "❌"

    context = {
        'date': date,
        'real_bill': real_bill,
        'daily_report_id': daily_report_id,

        # Table 1 Ta Phone
        'sumrealBillPhoneCount': sumrealBillPhoneCount,
        'sumrealBillPhone': sumrealBillPhone,
        'sumposTABillPhoneCount': sumposTABillPhoneCount,
        'sumposTABillPhone': sumposTABillPhone,
        'resultPhoneCashCount':resultPhoneCashCount,
        'resultPhoneCardCount':resultPhoneCardCount,
        'resultPhoneCash':resultPhoneCash,
        'resultPhoneCard':resultPhoneCard,
        'resultPhoneCount': resultPhoneCount,
        'resultPhone': resultPhone,
        'statusTableTaPhone': statusTableTaPhone,

        # Table 2 Dine-in
        'sumrealBillInCount': sumrealBillInCount,
        'sumrealBillIn': sumrealBillIn,
        'sumposInCount': sumposInCount,
        'sumposIn': sumposIn,
        'resultInCashCount':resultInCashCount,
        'resultInCardCount':resultInCardCount,
        'resultInCash':resultInCash,
        'resultInCard':resultInCard,
        'resultInCount': resultInCount,
        'resultIn': resultIn,
        'statusTableIn': statusTableIn,

        # Table 3 Ta Online
        'sumrealBillOnlineCount': sumrealBillOnlineCount,
        'sumrealBillOnline': sumrealBillOnline,


        'edcInCredit':edcInCredit,
    }
    return render(request,'keywordapp/lunch-result.html',context)

def LunchReport(request,daily_report_id):

    daily_object = get_object_or_404(DailyReportModel, id=daily_report_id)
    # Retrieve other related models or fields if needed

    date = daily_object.date
    real_bill_id = daily_object.real_bill.id
    edc_detail_id = daily_object.edc_detail.id
    pos_detail_id = daily_object.pos_detail.id
    delivery_detail_id = daily_object.delivery_detail.id

    real_bill = RealBillModel.objects.get(id=real_bill_id)
    realBillPhoneCash = real_bill.real_bill_phone_cash
    realBillPhoneCashCount = real_bill.real_bill_phone_cash_count
    realBillPhoneCard = real_bill.real_bill_phone_card
    realBillPhoneCardCount = real_bill.real_bill_phone_card_count
    realBillOnlineCash = real_bill.real_bill_online_cash
    realBillOnlineCashCount = real_bill.real_bill_online_cash_count
    realBillOnlineCard = real_bill.real_bill_online_card
    realBillOnlineCardCount = real_bill.real_bill_online_card_count
    realBillInCash = real_bill.real_bill_in_cash
    realBillInCashCount = real_bill.real_bill_in_cash_count
    realBillInCard = real_bill.real_bill_in_card
    realBillInCardCount = real_bill.real_bill_in_card_count
    posTABillPhoneCash = real_bill.pos_ta_bill_phone_cash
    posTABillPhoneCashCount = real_bill.pos_ta_bill_phone_cash_count
    posTABillPhoneCard = real_bill.pos_ta_bill_phone_card
    posTABillPhoneCardCount = real_bill.pos_ta_bill_phone_card_count
    posInCash = real_bill.pos_in_bill_cash
    posInCashCount = real_bill.pos_in_bill_cash_count
    posInCard = real_bill.pos_in_bill_card
    posInCardCount = real_bill.pos_in_bill_card_count
    edcInCredit = real_bill.edc_in_credit
    detailStatus = real_bill.detail_status


    # Summary
    # Table 1 TA Phone
    sumrealBillPhoneCount = realBillPhoneCashCount + realBillPhoneCardCount
    sumrealBillPhone = realBillPhoneCash + realBillPhoneCard
    # Table 2 Dine-in
    sumrealBillInCount = realBillInCashCount + realBillInCardCount
    sumrealBillIn = realBillInCash + realBillInCard
    # Table 3 TA Online
    sumrealBillOnlineCount = realBillOnlineCashCount + realBillOnlineCardCount
    sumrealBillOnline = realBillOnlineCash + realBillOnlineCard
    # Summary all Lunch
    totalBillLunch = sumrealBillPhone + sumrealBillIn + sumrealBillOnline
    context = {
        'date': date,
        'real_bill': real_bill,
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

def HomeResult(request):
    return render(request,'keywordapp/home-result.html')
def DinnerInput(request):
    return render(request,'keywordapp/dinner-input.html')
