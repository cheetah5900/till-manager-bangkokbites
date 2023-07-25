
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
        if mode == 'dinner':
            return redirect(reverse('dinner-input-quick', kwargs={'daily_report_id': daily_report.id}))


    return render(request, 'keywordapp/index.html', context)


def HomeInput(request):

    return render(request,'keywordapp/home-input.html')

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

def LunchResult(request,daily_report_id):

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
    realBillInCash = bill_lunch.real_bill_in_cash
    realBillInCashCount = bill_lunch.real_bill_in_cash_count
    realBillInCard = bill_lunch.real_bill_in_card
    realBillInCardCount = bill_lunch.real_bill_in_card_count
    posTABillPhoneCash = bill_lunch.pos_ta_bill_phone_cash
    posTABillPhoneCashCount = bill_lunch.pos_ta_bill_phone_cash_count
    posTABillPhoneCard = bill_lunch.pos_ta_bill_phone_card
    posTABillPhoneCardCount = bill_lunch.pos_ta_bill_phone_card_count
    posInCash = bill_lunch.pos_in_bill_cash
    posInCashCount = bill_lunch.pos_in_bill_cash_count
    posInCard = bill_lunch.pos_in_bill_card
    posInCardCount = bill_lunch.pos_in_bill_card_count
    edcInCredit = bill_lunch.edc_in_credit
    detailStatus = bill_lunch.detail_status

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
    sumrealBillOnlineCount = realBillOnlineCashCount + realBillOnlineCardCount
    sumrealBillOnline = realBillOnlineCash + realBillOnlineCard
    sumposTABillPhoneCount = posTABillPhoneCashCount + posTABillPhoneCardCount
    sumposTABillPhone = posTABillPhoneCash + posTABillPhoneCard
    # Table 2 Dine-in
    sumrealBillInCount = realBillInCashCount + realBillInCardCount
    sumrealBillIn = realBillInCash + realBillInCard
    sumposInCount = posInCashCount + posInCardCount
    sumposIn = posInCash + posInCard

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
        statusTableTa = "✅"
    else:
        statusTableTa = "❌"
    # Table 2 Dine-in
    if resultInCashCount == "✅" and resultInCardCount == "✅" and resultInCash == "✅" and resultInCard == "✅" and resultInCount == "✅" and resultIn == "✅":
        statusTableIn = "✅"
    else:
        statusTableIn = "❌"

    sumBillPhoneCard = posTABillPhoneCard + posInCard + realBillOnlineCard

    context = {
        'date': date,
        'bill_lunch': bill_lunch,
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
        'statusTableTa': statusTableTa,

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
        'sumBillPhoneCard':sumBillPhoneCard,
    }
    return render(request,'keywordapp/lunch-result.html',context)

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

    daily_object = get_object_or_404(DailyReportModel, id=daily_report_id)
    date = daily_object.date
    bill_dinner_id = daily_object.bill_dinner.id
    bill_lunch_id = daily_object.bill_lunch.id

    bill_dinner =  BillDinnerModel.objects.get(id=bill_dinner_id)
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
        # Home
        realBillHomePhoneCashCount = request.POST.get('real_bill_home_phone_cash_count')
        realBillHomePhoneCash = request.POST.get('real_bill_home_phone_cash')
        realBillHomePhoneCardCount = request.POST.get('real_bill_home_phone_card_count')
        realBillHomePhoneCard = request.POST.get('real_bill_home_phone_card')
        realBillHomeOnlineCashCount = request.POST.get('real_bill_home_online_cash_count')
        realBillHomeOnlineCash = request.POST.get('real_bill_home_online_cash')
        realBillHomeOnlineCardCount = request.POST.get('real_bill_home_online_card_count')
        realBillHomeOnlineCard = request.POST.get('real_bill_home_online_card')

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
        # Home  Phone
        bill_dinner.real_bill_home_phone_cash_count = realBillHomePhoneCashCount
        bill_dinner.real_bill_home_phone_cash = realBillHomePhoneCash
        bill_dinner.real_bill_home_phone_card_count = realBillHomePhoneCardCount
        bill_dinner.real_bill_home_phone_card = realBillHomePhoneCard
        # Home  Online
        bill_dinner.real_bill_home_online_cash_count = realBillHomeOnlineCashCount
        bill_dinner.real_bill_home_online_cash = realBillHomeOnlineCash
        bill_dinner.real_bill_home_online_card_count = realBillHomeOnlineCardCount
        bill_dinner.real_bill_home_online_card = realBillHomeOnlineCard
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
    realBillHomePhoneCard = bill_dinner.real_bill_home_phone_card
    realBillHomeOnlineCard = bill_dinner.real_bill_home_online_card
    edcInCredit = bill_dinner.edc_in_credit
    tipCredit = bill_dinner.tip_credit
    wrongCredit = bill_dinner.wrong_credit
    edcHomeCredit = bill_dinner.edc_home_credit

    # Calculate
    # Minus Home Phone Out From POS TA
    minusHomePhoneOutFromPosTa = posTABillPhoneCard - realBillHomePhoneCard
    # Sum 
    sumBillCardForEdcDineIn = minusHomePhoneOutFromPosTa + posInCard + realBillOnlineCard + tipCredit
    minusWrongCreditFromSumBillCard = sumBillCardForEdcDineIn - wrongCredit
    # Dinner EDC minus Lunch EDC
    edcInCreditResult = edcInCredit - edcInCreditLunch
    sumBillHomeCard = realBillHomePhoneCard + realBillHomeOnlineCard
    # Compare
    resultCheckEqual1 = "✅" if minusWrongCreditFromSumBillCard == edcInCreditResult else "❌"
    resultCheckEqual2 = "✅" if sumBillHomeCard == edcHomeCredit else "❌"

    context = {
        'date': date,
        'bill_dinner': bill_dinner,
        'posInCard': posInCard,
        'posTABillPhoneCard': posTABillPhoneCard,
        'realBillOnlineCard': realBillOnlineCard,
        'sumBillCardForEdcDineIn': sumBillCardForEdcDineIn,
        'sumBillHomeCard': sumBillHomeCard,
        'realBillHomePhoneCard': realBillHomePhoneCard,
        'minusHomePhoneOutFromPosTa': minusHomePhoneOutFromPosTa,
        'minusWrongCreditFromSumBillCard': minusWrongCreditFromSumBillCard,
        'resultCheckEqual1': resultCheckEqual1,
        'resultCheckEqual2': resultCheckEqual2,
        'edcInCredit': edcInCredit,
        'edcInCreditLunch': edcInCreditLunch,
        'edcInCreditResult': edcInCreditResult,
        'daily_report_id': daily_report_id,
    }
    return render(request, 'keywordapp/dinner-input-detail.html', context)

def DinnerResult(request,daily_report_id):

    daily_object = get_object_or_404(DailyReportModel, id=daily_report_id)
    # Retrieve other related models or fields if needed

    date = daily_object.date
    bill_dinner_id = daily_object.bill_dinner.id

    bill_dinner =  BillDinnerModel.objects.get(id=bill_dinner_id)
    realBillPhoneCash = bill_dinner.real_bill_phone_cash
    realBillPhoneCashCount = bill_dinner.real_bill_phone_cash_count
    realBillPhoneCard = bill_dinner.real_bill_phone_card
    realBillPhoneCardCount = bill_dinner.real_bill_phone_card_count
    realBillOnlineCash = bill_dinner.real_bill_online_cash
    realBillOnlineCashCount = bill_dinner.real_bill_online_cash_count
    realBillOnlineCard = bill_dinner.real_bill_online_card
    realBillOnlineCardCount = bill_dinner.real_bill_online_card_count
    realBillInCash = bill_dinner.real_bill_in_cash
    realBillInCashCount = bill_dinner.real_bill_in_cash_count
    realBillInCard = bill_dinner.real_bill_in_card
    realBillInCardCount = bill_dinner.real_bill_in_card_count
    # Home Phone
    realBillHomePhoneCashCount = bill_dinner.real_bill_home_phone_cash_count
    realBillHomePhoneCash = bill_dinner.real_bill_home_phone_cash
    realBillHomePhoneCardCount = bill_dinner.real_bill_home_phone_card_count
    realBillHomePhoneCard = bill_dinner.real_bill_home_phone_card
    # Home Online
    realBillHomeOnlineCashCount = bill_dinner.real_bill_home_online_cash_count
    realBillHomeOnlineCash = bill_dinner.real_bill_home_online_cash
    realBillHomeOnlineCardCount = bill_dinner.real_bill_home_online_card_count
    realBillHomeOnlineCard = bill_dinner.real_bill_home_online_card
    posTABillPhoneCash = bill_dinner.pos_ta_bill_phone_cash
    posTABillPhoneCashCount = bill_dinner.pos_ta_bill_phone_cash_count
    posTABillPhoneCard = bill_dinner.pos_ta_bill_phone_card
    posTABillPhoneCardCount = bill_dinner.pos_ta_bill_phone_card_count
    posInCash = bill_dinner.pos_in_bill_cash
    posInCashCount = bill_dinner.pos_in_bill_cash_count
    posInCard = bill_dinner.pos_in_bill_card
    posInCardCount = bill_dinner.pos_in_bill_card_count
    edcInCredit = bill_dinner.edc_in_credit
    detailStatus = bill_dinner.detail_status

    # Status
    # Table 1 TA Phone
    resultPhoneCashCount = "✅" if realBillPhoneCashCount + realBillHomePhoneCashCount  == posTABillPhoneCashCount else "❌"
    resultPhoneCardCount = "✅" if realBillPhoneCardCount + realBillHomePhoneCardCount == posTABillPhoneCardCount else "❌"
    resultPhoneCash = "✅" if realBillPhoneCash + realBillHomePhoneCash == posTABillPhoneCash else "❌"
    resultPhoneCard = "✅" if realBillPhoneCard + realBillHomePhoneCard == posTABillPhoneCard else "❌"

    # Table 2 Dine-in
    resultInCashCount = "✅" if realBillInCashCount == posInCashCount else "❌"
    resultInCardCount = "✅" if realBillInCardCount == posInCardCount else "❌"
    resultInCash = "✅" if realBillInCash == posInCash else "❌"
    resultInCard = "✅" if realBillInCard == posInCard else "❌"

    # Summary
    # Table 1 TA Phone + Home Phone
    sumrealBillPhoneCount = realBillPhoneCashCount + realBillPhoneCardCount
    sumrealBillPhone = realBillPhoneCash + realBillPhoneCard
    sumrealBillHomePhoneCount = realBillHomePhoneCashCount + realBillHomePhoneCardCount
    sumrealBillHomePhone = realBillHomePhoneCash + realBillHomePhoneCard
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
    sumrealBillhomeOnlineCount = realBillHomeOnlineCashCount + realBillHomeOnlineCardCount
    sumrealBillhomeOnline = realBillHomeOnlineCash + realBillHomeOnlineCard

    # Table 4 Conclusions

    sumBillPhoneCard = posTABillPhoneCard + posInCard + realBillOnlineCard
    minusHomeFromPhone = sumBillPhoneCard - realBillHomePhoneCard

    # Check equality 
    # TABLE 1 TA Phone
    resultPhoneCount = "✅" if sumrealBillPhoneCount + sumrealBillHomePhoneCount == sumposTABillPhoneCount else "❌"
    resultPhone = "✅" if sumrealBillPhone + sumrealBillHomePhone == sumposTABillPhone else "❌"
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
        'bill_dinner': bill_dinner,
        'daily_report_id': daily_report_id,

        # Table 1 Ta Phone
        'sumrealBillPhoneCount': sumrealBillPhoneCount,
        'sumrealBillPhone': sumrealBillPhone,
        'sumrealBillHomePhoneCount': sumrealBillHomePhoneCount,
        'sumrealBillHomePhone': sumrealBillHomePhone,
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
        'sumrealBillhomeOnlineCount': sumrealBillhomeOnlineCount,
        'sumrealBillhomeOnline': sumrealBillhomeOnline,

        # Table 4 Conclusion
        'sumBillPhoneCard': sumBillPhoneCard,
        'minusHomeFromPhone': minusHomeFromPhone,
        

        'edcInCredit':edcInCredit,
    }
    return render(request,'keywordapp/dinner-result.html',context)

def DinnerReport(request,daily_report_id):

    daily_object = get_object_or_404(DailyReportModel, id=daily_report_id)
    # Retrieve other related models or fields if needed

    date = daily_object.date
    bill_lunch_id = daily_object.bill_lunch.id
    bill_dinner_id = daily_object.bill_dinner.id

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

    #* "Reformat" amount lunch
    realBillPhoneCashLunchReformat = intcomma(bill_lunch.real_bill_phone_cash)
    realBillPhoneCardLunchReformat = intcomma(bill_lunch.real_bill_phone_card)
    realBillOnlineCashLunchReformat = intcomma(bill_lunch.real_bill_online_cash)
    realBillOnlineCardLunchReformat = intcomma(bill_lunch.real_bill_online_card)
    realBillInCashLunchReformat = intcomma(bill_lunch.real_bill_in_cash)
    realBillInCardLunchReformat = intcomma(bill_lunch.real_bill_in_card)

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
    # Home Phone
    realBillHomePhoneCashCountDinner = bill_dinner.real_bill_home_phone_cash_count
    realBillHomePhoneCashDinner = bill_dinner.real_bill_home_phone_cash
    realBillHomePhoneCardCountDinner = bill_dinner.real_bill_home_phone_card_count
    realBillHomePhoneCardDinner = bill_dinner.real_bill_home_phone_card
    # Home Online
    realBillHomeOnlineCashCountDinner = bill_dinner.real_bill_home_online_cash_count
    realBillHomeOnlineCashDinner = bill_dinner.real_bill_home_online_cash
    realBillHomeOnlineCardCountDinner = bill_dinner.real_bill_home_online_card_count
    realBillHomeOnlineCardDinner = bill_dinner.real_bill_home_online_card

    #* "Reformat" amount dinner
    realBillPhoneCashDinnerReformat = intcomma(bill_dinner.real_bill_phone_cash)
    realBillPhoneCardDinnerReformat = intcomma(bill_dinner.real_bill_phone_card)
    realBillOnlineCashDinnerReformat = intcomma(bill_dinner.real_bill_online_cash)
    realBillOnlineCardDinnerReformat = intcomma(bill_dinner.real_bill_online_card)
    realBillInCashDinnerReformat = intcomma(bill_dinner.real_bill_in_cash)
    realBillInCardDinnerReformat = intcomma(bill_dinner.real_bill_in_card)
    # Home Phone
    realBillHomePhoneCashDinnerReformat = intcomma(bill_dinner.real_bill_home_phone_cash)
    realBillHomePhoneCardDinnerReformat = intcomma(bill_dinner.real_bill_home_phone_card)
    # Home Online
    realBillHomeOnlineCashDinnerReformat = intcomma(bill_dinner.real_bill_home_online_cash)
    realBillHomeOnlineCardDinnerReformat = intcomma(bill_dinner.real_bill_home_online_card)

    #? Summary
    totalBillLunch = realBillPhoneCashLunch + realBillPhoneCardLunch + realBillInCashLunch + realBillInCardLunch + realBillOnlineCashLunch + realBillOnlineCardLunch
    totalBillLunchReformat = intcomma(realBillPhoneCashLunch + realBillPhoneCardLunch + realBillInCashLunch + realBillInCardLunch + realBillOnlineCashLunch + realBillOnlineCardLunch)
    sumTotal = realBillOnlineCashLunch + realBillOnlineCardLunch + realBillPhoneCashLunch + realBillPhoneCardLunch + realBillInCashLunch + realBillInCardLunch + realBillHomePhoneCashDinner + realBillHomePhoneCardDinner + realBillHomeOnlineCashDinner + realBillHomeOnlineCardDinner + realBillPhoneCashDinner + realBillPhoneCardDinner + realBillOnlineCashDinner + realBillOnlineCardDinner + realBillInCashDinner + realBillInCardDinner
    sumTotalReformat = intcomma(realBillOnlineCashLunch + realBillOnlineCardLunch + realBillPhoneCashLunch + realBillPhoneCardLunch + realBillInCashLunch + realBillInCardLunch + realBillHomePhoneCashDinner + realBillHomePhoneCardDinner + realBillHomeOnlineCashDinner + realBillHomeOnlineCardDinner + realBillPhoneCashDinner + realBillPhoneCardDinner + realBillOnlineCashDinner + realBillOnlineCardDinner + realBillInCashDinner + realBillInCardDinner)
    totalBillDinner = intcomma(sumTotal - totalBillLunch)
    sumCash = intcomma(realBillOnlineCashLunch + realBillPhoneCashLunch + realBillInCashLunch + realBillHomePhoneCashDinner + realBillHomeOnlineCashDinner + realBillPhoneCashDinner + realBillOnlineCashDinner + realBillInCashDinner)
    sumCard = intcomma(realBillOnlineCardLunch + realBillPhoneCardLunch + realBillInCardLunch + realBillHomePhoneCardDinner + realBillHomeOnlineCardDinner + realBillPhoneCardDinner + realBillOnlineCardDinner + realBillInCardDinner)
    sumTip = intcomma(tipLunch + tipDinner)
    sumWrongCredit = intcomma(wrongCreditLunch + wrongCreditDinner)
    sumrealBillOnlineCountDinner = intcomma(realBillOnlineCashCountDinner + realBillOnlineCardCountDinner)
    sumrealBillHomeOnlineCountDinner = intcomma(realBillHomeOnlineCashCountDinner + realBillHomeOnlineCardCountDinner)
    totalOnlineCount = intcomma(realBillOnlineCardCountLunch + realBillOnlineCashCountLunch + realBillOnlineCashCountDinner + realBillOnlineCardCountDinner + realBillHomeOnlineCashCountDinner + realBillHomeOnlineCardCountDinner)
    totalOnlineAmount = intcomma(realBillOnlineCardLunch + realBillOnlineCashLunch + realBillOnlineCashDinner + realBillOnlineCardDinner + realBillHomeOnlineCashDinner + realBillHomeOnlineCardDinner)


    context = {
        'date': date,
        'daily_report_id': daily_report_id,
        #! Lunch
        # Row 1 Ta Online Lunch
        'sumrealBillOnlineCount': realBillOnlineCashCountLunch + realBillOnlineCardCountLunch,
        'sumrealBillOnline': intcomma(realBillOnlineCashLunch + realBillOnlineCardLunch),
        'realBillOnlineCashLunchReformat': realBillOnlineCashLunchReformat,
        'realBillOnlineCardLunchReformat': realBillOnlineCardLunchReformat,
        # Row 2 Ta Phone Lunch
        'sumrealBillPhoneCount': realBillPhoneCashCountLunch + realBillPhoneCardCountLunch - realBillTaPhoneDividePayCountLunch,
        'sumrealBillPhone': intcomma(realBillPhoneCashLunch + realBillPhoneCardLunch),
        'realBillPhoneCashLunchReformat': realBillPhoneCashLunchReformat,
        'realBillPhoneCardLunchReformat': realBillPhoneCardLunchReformat,
        # Row 3 Dine-in Lunch
        'sumrealBillInCount': realBillInCashCountLunch + realBillInCardCountLunch - realBillDineInDividePayCountLunch,
        'sumrealBillIn': intcomma(realBillInCashLunch + realBillInCardLunch),
        'realBillInCashLunchReformat': realBillInCashLunchReformat,
        'realBillInCardLunchReformat': realBillInCardLunchReformat,
        #! Dinner
        # Row 4 Home Phone
        'sumrealBillHomePhoneCountDinner': realBillHomePhoneCashCountDinner + realBillHomePhoneCardCountDinner,
        'sumrealBillHomePhoneDinner': intcomma(realBillHomePhoneCashDinner + realBillHomePhoneCardDinner),
        'realBillHomePhoneCashDinnerReformat': realBillHomePhoneCashDinnerReformat,
        'realBillHomePhoneCardDinnerReformat': realBillHomePhoneCardDinnerReformat,
        # Row 5 Home Online
        'sumrealBillHomeOnlineCountDinner': sumrealBillHomeOnlineCountDinner,
        'sumrealBillHomeOnlineDinner': intcomma(realBillHomeOnlineCashDinner + realBillHomeOnlineCardDinner),
        'realBillHomeOnlineCashDinnerReformat': realBillHomeOnlineCashDinnerReformat,
        'realBillHomeOnlineCardDinnerReformat': realBillHomeOnlineCardDinnerReformat,
        # Row 6 T/A Phone Dinner
        'sumrealBillPhoneCountDinner': realBillPhoneCashCountDinner + realBillPhoneCardCountDinner - realBillTaPhoneDividePayCountDinner,
        'sumrealBillPhoneDinner': intcomma(realBillPhoneCashDinner + realBillPhoneCardDinner),
        'realBillPhoneCashDinnerReformat': realBillPhoneCashDinnerReformat,
        'realBillPhoneCardDinnerReformat': realBillPhoneCardDinnerReformat,
        # Row 7 T/A Online Dinner
        'sumrealBillOnlineCountDinner': sumrealBillOnlineCountDinner,
        'sumrealBillOnlineDinner': intcomma(realBillOnlineCashDinner + realBillOnlineCardDinner),
        'realBillOnlineCashDinnerReformat': realBillOnlineCashDinnerReformat,
        'realBillOnlineCardDinnerReformat': realBillOnlineCardDinnerReformat,
        # Row 8 Dine-in Dinner
        'sumrealBillInCountDinner': realBillInCashCountDinner + realBillInCardCountDinner - realBillDineInDividePayCountDinner,
        'sumrealBillInDinner': intcomma(realBillInCashDinner + realBillInCardDinner),
        'realBillInCashDinnerReformat': realBillInCashDinnerReformat,
        'realBillInCardDinnerReformat': realBillInCardDinnerReformat,
        #! Total
        'totalBillLunchReformat': totalBillLunchReformat,
        'totalBillDinner': totalBillDinner,
        'sumTotalReformat': sumTotalReformat,
        'sumCash': sumCash,
        'sumCard': sumCard,
        'sumTip': sumTip,
        'sumWrongCredit': sumWrongCredit,
        'totalOnlineAmount': totalOnlineAmount,
        'totalOnlineCount': totalOnlineCount,
        
    }
    return render(request,'keywordapp/dinner-report.html',context)

def HomeResult(request):
    return render(request,'keywordapp/home-result.html')
def DinnerInput(request):
    return render(request,'keywordapp/dinner-input.html')
