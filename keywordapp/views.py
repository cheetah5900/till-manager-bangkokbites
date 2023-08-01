
# =============================== FOR PAGE KEYWORD MANAGER ===============================
# =============================== FOR PAGE KEYWORD MANAGER ===============================
# =============================== FOR PAGE KEYWORD MANAGER ===============================

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils import timezone
import time
import datetime

from decimal import Decimal

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from django.contrib.humanize.templatetags.humanize import intcomma

# require login to enter function
# import model
from keywordapp.models import *

# IMAGE
import os
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont


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
            bill_lunch = BillLunchModel.objects.create()
            bill_dinner = BillDinnerModel.objects.create()

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
        if mode == 'disburse':
            return redirect(reverse('disburse-list', kwargs={'daily_report_id': daily_report.id}))

    return render(request, 'keywordapp/index.html', context)

#! DISBURSE


def DisburseList(request, daily_report_id):

    daily_report = get_object_or_404(DailyReportModel, id=daily_report_id)
    date = daily_report.date

    totalDisburse = 0
    # You can also access the related DeliveryDetailModel instances from a DailyReportModel instance
    related_disburse_details = daily_report.bill_dinner.disbursemodel_set.all()
    for detail in related_disburse_details:
        totalDisburse += detail.price
    context = {
        'date': date,
        'daily_report_id': daily_report_id,
        'totalDisburse': totalDisburse,
        'related_disburse_details': related_disburse_details,
    }
    return render(request, 'keywordapp/disburse-list.html', context)


def DisburseInput(request, daily_report_id, disburse_id):

    daily_report = get_object_or_404(DailyReportModel, id=daily_report_id)
    date = daily_report.date
    bill_dinner = daily_report.bill_dinner
    if disburse_id == 0:
        newDisburse = DisburseModel.objects.create(bill_dinner=bill_dinner)
        newDisburseId = newDisburse.id
        return redirect(reverse('disburse-input', kwargs={'daily_report_id': daily_report_id, 'disburse_id': newDisburseId}))

    if request.method == 'POST':
        # Home
        name = request.POST.get('name')
        price = request.POST.get('price')

        disburse_detail = DisburseModel.objects.get(id=disburse_id)

        disburse_detail.name = name
        disburse_detail.price = price
        disburse_detail.save()

        return redirect(reverse('disburse-list', kwargs={'daily_report_id': daily_report_id}))

    disburse_detail = DisburseModel.objects.get(id=disburse_id)

    context = {
        'date': date,
        'daily_report_id': daily_report_id,
        'disburse_detail': disburse_detail,
    }
    return render(request, 'keywordapp/disburse-input.html', context)

#! LUNCH


def LunchInputQuick(request, daily_report_id):

    daily_report = get_object_or_404(DailyReportModel, id=daily_report_id)
    date = daily_report.date
    bill_lunch_id = daily_report.bill_lunch.id

    bill_lunch = BillLunchModel.objects.get(id=bill_lunch_id)

    if request.method == 'POST':
        posTABillPhoneCard = request.POST.get('pos_ta_bill_phone_card')
        posInCard = request.POST.get('pos_in_bill_card')
        edcInCredit = request.POST.get('edc_in_credit')
        tipCredit = request.POST.get('tip_credit')
        wrongCredit = request.POST.get('wrong_credit')

        bill_lunch = get_object_or_404(BillLunchModel, id=bill_lunch_id)
        bill_lunch.pos_ta_bill_phone_card = posTABillPhoneCard
        bill_lunch.pos_in_bill_card = posInCard
        bill_lunch.edc_in_credit = edcInCredit
        bill_lunch.tip_credit = tipCredit
        bill_lunch.wrong_credit = wrongCredit
        bill_lunch.detail_status = 1

        # Save the updated object
        bill_lunch.save()

        return redirect(reverse('lunch-input-detail', kwargs={'daily_report_id': daily_report_id}))

    return render(request, 'keywordapp/lunch-input-quick.html', context={'date': date, 'bill_lunch': bill_lunch})


def LunchInputDetail(request, daily_report_id):

    daily_object = get_object_or_404(DailyReportModel, id=daily_report_id)
    date = daily_object.date
    bill_lunch_id = daily_object.bill_lunch.id

    bill_lunch = BillLunchModel.objects.get(id=bill_lunch_id)

    if request.method == 'POST':
        posTABillPhoneCash = request.POST.get('pos_ta_bill_phone_cash')
        posTABillPhoneCashCount = request.POST.get(
            'pos_ta_bill_phone_cash_count')
        posTABillPhoneCard = request.POST.get('pos_ta_bill_phone_card')
        posTABillPhoneCardCount = request.POST.get(
            'pos_ta_bill_phone_card_count')
        posInCash = request.POST.get('pos_in_bill_cash')
        posInCashCount = request.POST.get('pos_in_bill_cash_count')
        posInCard = request.POST.get('pos_in_bill_card')
        posInCardCount = request.POST.get('pos_in_bill_card_count')
        realBillTaPhoneDividePayCount = request.POST.get(
            'real_bill_taphone_dividepay_count')
        realBillDineInDividePayCount = request.POST.get(
            'real_bill_dinein_dividepay_count')
        realBillInCashCount = posInCashCount
        realBillInCash = posInCash
        realBillInCardCount = posInCardCount
        realBillInCard = posInCard
        realBillPhoneCashCount = posTABillPhoneCashCount
        realBillPhoneCash = posTABillPhoneCash
        realBillPhoneCardCount = posTABillPhoneCardCount
        realBillPhoneCard = posTABillPhoneCard

        edcInCredit = request.POST.get('edc_in_credit')

        bill_lunch = get_object_or_404(BillLunchModel, id=bill_lunch_id)

        # Real Bill TA Phone
        bill_lunch.real_bill_phone_cash_count = realBillPhoneCashCount
        bill_lunch.real_bill_phone_cash = realBillPhoneCash
        bill_lunch.real_bill_phone_card_count = realBillPhoneCardCount
        bill_lunch.real_bill_phone_card = realBillPhoneCard
        bill_lunch.real_bill_taphone_dividepay_count = realBillTaPhoneDividePayCount
        bill_lunch.real_bill_dinein_dividepay_count = realBillDineInDividePayCount
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
        return redirect(reverse('lunch-report', kwargs={'daily_report_id': daily_report_id}))

    date = daily_object.date
    bill_lunch_id = daily_object.bill_lunch.id

    bill_lunch = BillLunchModel.objects.get(id=bill_lunch_id)

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
        'posInCard': posInCard,
        'addTipToSum': addTipToSum,
        'minusWrongCreditFromSumBillCard': minusWrongCreditFromSumBillCard,
        'posTABillPhoneCard': posTABillPhoneCard,
        'realBillOnlineCard': realBillOnlineCard,
        'sumBillPhoneCard': sumBillPhoneCard,
        'resultCheckEqual': resultCheckEqual,
        'edcInCredit': edcInCredit,
        'daily_report_id': daily_report_id,
    }
    return render(request, 'keywordapp/lunch-input-detail.html', context)


def LunchReport(request, daily_report_id):

    daily_object = get_object_or_404(DailyReportModel, id=daily_report_id)
    # Retrieve other related models or fields if needed

    date = daily_object.date
    bill_lunch_id = daily_object.bill_lunch.id

    bill_lunch = BillLunchModel.objects.get(id=bill_lunch_id)
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
    sumrealBillPhoneCount = realBillPhoneCashCount + \
        realBillPhoneCardCount - realBillTaPhoneDividePayCount
    sumrealBillPhone = realBillPhoneCash + realBillPhoneCard
    # Row 3 Dine-in Lunch
    sumrealBillInCount = realBillInCashCount + \
        realBillInCardCount - realBillDineInDividePayCount
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




        'edcInCredit': edcInCredit,
    }
    return render(request, 'keywordapp/lunch-report.html', context)

#! DINNER


def DinnerInputQuick(request, daily_report_id):

    daily_object = get_object_or_404(DailyReportModel, id=daily_report_id)
    date = daily_object.date
    bill_dinner_id = daily_object.bill_dinner.id

    bill_dinner = BillDinnerModel.objects.get(id=bill_dinner_id)

    if request.method == 'POST':
        realBillOnlineCard = request.POST.get('real_bill_online_card')
        posTABillPhoneCard = request.POST.get('pos_ta_bill_phone_card')
        realBillHomePhoneCard = request.POST.get('real_bill_home_phone_card')
        realBillHomeOnlineCard = request.POST.get('real_bill_home_online_card')
        posInCard = request.POST.get('pos_in_bill_card')
        edcInCredit = request.POST.get('edc_in_credit')
        edcInMotoCredit = request.POST.get('edc_in_moto_credit')
        tipCredit = request.POST.get('tip_credit')
        wrongCredit = request.POST.get('wrong_credit')
        exceedCredit = request.POST.get('exceed_credit')
        edcHomeCredit = request.POST.get('edc_home_credit')

        bill_dinner = get_object_or_404(BillDinnerModel, id=bill_dinner_id)
        bill_dinner.real_bill_online_card = realBillOnlineCard
        bill_dinner.pos_ta_bill_phone_card = posTABillPhoneCard
        bill_dinner.pos_in_bill_card = posInCard
        bill_dinner.real_bill_home_phone_card = realBillHomePhoneCard
        bill_dinner.real_bill_home_online_card = realBillHomeOnlineCard
        bill_dinner.edc_in_moto_credit = edcInMotoCredit

        bill_dinner.exceed_credit = exceedCredit
        bill_dinner.wrong_credit = wrongCredit
        bill_dinner.tip_credit = tipCredit
        bill_dinner.edc_in_credit = edcInCredit
        bill_dinner.edc_home_credit = edcHomeCredit
        bill_dinner.detail_status = 1

        # Save the updated object
        bill_dinner.save()

        return redirect(reverse('dinner-input-detail', kwargs={'daily_report_id': daily_report_id}))

    return render(request, 'keywordapp/dinner-input-quick.html', context={'date': date, 'bill_dinner': bill_dinner})


def DinnerInputDetail(request, daily_report_id):

    daily_report = get_object_or_404(DailyReportModel, id=daily_report_id)
    date = daily_report.date
    bill_dinner_id = daily_report.bill_dinner.id
    bill_lunch_id = daily_report.bill_lunch.id

    bill_dinner = BillDinnerModel.objects.get(id=bill_dinner_id)
    bill_lunch = BillLunchModel.objects.get(id=bill_lunch_id)

    # Access the related DeliveryDetailModel instances using the foreign key relationship
    related_delivery_details = daily_report.bill_dinner.deliverydetailmodel_set.all()

    # Calculate the sum of the real_bill_home_oa_amount attribute for all DeliveryDetailModel instances
    realBillHomePhoneCashCount = sum(
        detail.real_bill_home_phone_cash_count for detail in related_delivery_details)
    realBillHomePhoneCash = sum(
        detail.real_bill_home_phone_cash for detail in related_delivery_details)
    realBillHomePhoneCardCount = sum(
        detail.real_bill_home_phone_card_count for detail in related_delivery_details)
    realBillHomePhoneCard = sum(
        detail.real_bill_home_phone_card for detail in related_delivery_details)
    realBillHomeOnlineCard = sum(
        detail.real_bill_home_online_card for detail in related_delivery_details)
    sumEdcHomeCard = sum(
        detail.edc_home_credit for detail in related_delivery_details)
    sumEdcMotoCard = sum(
        detail.moto_credit for detail in related_delivery_details)

    if request.method == 'POST':
        realBillOnlineCash = request.POST.get('real_bill_online_cash')
        realBillOnlineCashCount = request.POST.get(
            'real_bill_online_cash_count')
        realBillOnlineCard = request.POST.get('real_bill_online_card')
        realBillOnlineCardCount = request.POST.get(
            'real_bill_online_card_count')
        posTABillPhoneCash = request.POST.get('pos_ta_bill_phone_cash')
        posTABillPhoneCashCount = request.POST.get(
            'pos_ta_bill_phone_cash_count')
        posTABillPhoneCard = request.POST.get('pos_ta_bill_phone_card')
        posTABillPhoneCardCount = request.POST.get(
            'pos_ta_bill_phone_card_count')
        posInCash = request.POST.get('pos_in_bill_cash')
        posInCashCount = request.POST.get('pos_in_bill_cash_count')
        posInCard = request.POST.get('pos_in_bill_card')
        posInCardCount = request.POST.get('pos_in_bill_card_count')
        realBillTaPhoneDividePayCount = request.POST.get(
            'real_bill_taphone_dividepay_count')
        realBillDineInDividePayCount = request.POST.get(
            'real_bill_dinein_dividepay_count')
        realBillInCashCount = posInCashCount
        realBillInCash = posInCash
        realBillInCardCount = posInCardCount
        realBillInCard = posInCard

        wrongCredit = request.POST.get('wrong_credit')
        tipCredit = request.POST.get('tip_credit')
        edcInCredit = request.POST.get('edc_in_credit')

        # Calculation
        realBillPhoneCashCount = int(
            posTABillPhoneCashCount) - int(realBillHomePhoneCashCount)
        realBillPhoneCash = Decimal(
            posTABillPhoneCash) - Decimal(realBillHomePhoneCash)
        realBillPhoneCardCount = int(
            posTABillPhoneCardCount) - int(realBillHomePhoneCardCount)
        realBillPhoneCard = Decimal(
            posTABillPhoneCard) - Decimal(realBillHomePhoneCard)

        bill_dinner = get_object_or_404(BillDinnerModel, id=bill_dinner_id)

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

    # get data for general data LUNCH
    edcInCreditLunch = bill_lunch.edc_in_credit

    # get data for general data DINNER
    posTABillPhoneCard = bill_dinner.pos_ta_bill_phone_card
    posInCard = bill_dinner.pos_in_bill_card
    realBillOnlineCard = bill_dinner.real_bill_online_card
    edcInCredit = bill_dinner.edc_in_credit
    edcInMotoCredit = sum(
        detail.moto_credit for detail in related_delivery_details)
    tipCredit = bill_dinner.tip_credit
    wrongCredit = bill_dinner.wrong_credit

    # Calculate
    # Minus Home Phone Out From POS TA
    minusHomePhoneOutFromPosTa = posTABillPhoneCard - realBillHomePhoneCard
    # Sum
    sumBillCardForEdcDineIn = minusHomePhoneOutFromPosTa + posInCard + \
        realBillOnlineCard + tipCredit + edcInMotoCredit + edcInCreditLunch
    minusWrongCreditFromSumBillCard = sumBillCardForEdcDineIn - wrongCredit
    sumBillHomeCard = realBillHomePhoneCard + realBillHomeOnlineCard
    minusMotoCreditFromSumBillHomeCard = sumBillHomeCard - edcInMotoCredit
    # Compare
    resultCheckEqual1 = "✅" if minusWrongCreditFromSumBillCard == edcInCredit else "❌"
    resultCheckEqual2 = "✅" if minusMotoCreditFromSumBillHomeCard == sumEdcHomeCard else "❌"

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
        'resultCheckEqual2': resultCheckEqual2,
        'edcInCredit': edcInCredit,
        'edcInCreditLunch': edcInCreditLunch,
        'edcInMotoCredit': edcInMotoCredit,
        # Home
        'realBillHomePhoneCard': realBillHomePhoneCard,
        'realBillHomeOnlineCard': realBillHomeOnlineCard,
        'sumBillHomeCard': sumBillHomeCard,
        'minusMotoCreditFromSumBillHomeCard': minusMotoCreditFromSumBillHomeCard,
        'sumEdcHomeCard': sumEdcHomeCard,
        'sumEdcMotoCard': sumEdcMotoCard,
        'daily_report_id': daily_report_id,
    }
    return render(request, 'keywordapp/dinner-input-detail.html', context)


def DinnerReport(request, daily_report_id):

    daily_report = get_object_or_404(DailyReportModel, id=daily_report_id)
    # Retrieve other related models or fields if needed

    date = daily_report.date
    day = date.strftime("%A")
    dateForImage = date.strftime("%d / %m / %y")

    bill_lunch_id = daily_report.bill_lunch.id
    bill_dinner_id = daily_report.bill_dinner.id

    # * Lunch Data
    bill_lunch = BillLunchModel.objects.get(id=bill_lunch_id)
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

    # * Dinner Data
    bill_dinner = BillDinnerModel.objects.get(id=bill_dinner_id)
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

    # * Delivery Section
    # Access the related DeliveryDetailModel instances using the foreign key relationship
    related_delivery_details = daily_report.bill_dinner.deliverydetailmodel_set.all()

    # * Disburse Section
    related_disburse_details = daily_report.bill_dinner.disbursemodel_set.all()

    # Summarize the number of delivery man
    for detail in related_delivery_details:
        detail.sum_commission = int(detail.wage_per_home * (detail.real_bill_home_phone_cash_count +
                                    detail.real_bill_home_phone_card_count + detail.real_bill_home_online_cash_count + detail.real_bill_home_online_card_count))
        detail.home_count = detail.real_bill_home_phone_cash_count + detail.real_bill_home_phone_card_count + \
            detail.real_bill_home_online_cash_count + \
            detail.real_bill_home_online_card_count
        detail.sum_commission_and_oa = int(
            (detail.real_bill_home_oa_count * detail.real_bill_home_oa_amount) + detail.sum_commission)
        if detail.real_bill_home_oa_count > 0:
            detail.show_oa_count = " + " + \
                str(detail.real_bill_home_oa_count)+" OA"
        else: detail.show_oa_count = ''
        if detail.real_bill_home_oa_amount > 0:
            detail.show_oa_amount = " + " + \
                str(int(detail.real_bill_home_oa_amount))
        else: detail.show_oa_amount = ''

    # sum all without separating delivery man
    realBillHomePhoneCashCountDinner = sum(
        detail.real_bill_home_phone_cash_count for detail in related_delivery_details)
    realBillHomePhoneCashDinner = sum(
        detail.real_bill_home_phone_cash for detail in related_delivery_details)
    realBillHomePhoneCardCountDinner = sum(
        detail.real_bill_home_phone_card_count for detail in related_delivery_details)
    realBillHomePhoneCardDinner = sum(
        detail.real_bill_home_phone_card for detail in related_delivery_details)
    realBillHomeOnlineCashCountDinner = sum(
        detail.real_bill_home_online_cash_count for detail in related_delivery_details)
    realBillHomeOnlineCashDinner = sum(
        detail.real_bill_home_online_cash for detail in related_delivery_details)
    realBillHomeOnlineCardCountDinner = sum(
        detail.real_bill_home_online_card_count for detail in related_delivery_details)
    realBillHomeOnlineCardDinner = sum(
        detail.real_bill_home_online_card for detail in related_delivery_details)

    # ? Summary
    # * Report Section
    # Row 1 Ta Online Lunch
    totalBillLunch = realBillPhoneCashLunch + realBillPhoneCardLunch + realBillInCashLunch + \
        realBillInCardLunch + realBillOnlineCashLunch + realBillOnlineCardLunch
    sumrealBillOnlineCount = realBillOnlineCashCountLunch + realBillOnlineCardCountLunch
    sumrealBillOnline = realBillOnlineCashLunch + realBillOnlineCardLunch
    # Row 2 Ta Phone Lunch
    sumrealBillPhoneCount = realBillPhoneCashCountLunch + realBillPhoneCardCountLunch - realBillTaPhoneDividePayCountLunch
    realBillPhoneLunch = realBillPhoneCashLunch + realBillPhoneCardLunch
    # Row 3 Dine-in Lunch
    sumrealBillInCount = realBillInCashCountLunch + realBillInCardCountLunch - realBillDineInDividePayCountLunch
    sumrealBillIn = realBillInCashLunch + realBillInCardLunch
    # Row 10
    sumTotal = realBillOnlineCashLunch + realBillOnlineCardLunch + realBillPhoneCashLunch + realBillPhoneCardLunch + realBillInCashLunch + realBillInCardLunch + realBillHomePhoneCashDinner + realBillHomePhoneCardDinner + \
        realBillHomeOnlineCashDinner + realBillHomeOnlineCardDinner + realBillPhoneCashDinner + realBillPhoneCardDinner + \
        realBillOnlineCashDinner + realBillOnlineCardDinner + \
        realBillInCashDinner + realBillInCardDinner
    # Row 4
    sumrealBillHomePhoneDinner = realBillHomePhoneCashDinner + realBillHomePhoneCardDinner
    # Row 4 Home Phone
    sumrealBillHomePhoneCountDinner = realBillHomePhoneCashCountDinner + \
        realBillHomePhoneCardCountDinner
    # Row 5 Home Online
    sumrealBillHomeOnlineCountDinner = realBillHomeOnlineCashCountDinner + \
        realBillHomeOnlineCardCountDinner
    sumrealBillHomeOnlineDinner = realBillHomeOnlineCashDinner + realBillHomeOnlineCardDinner
    # Row 6 T/A Phone Dinner
    sumrealBillPhoneCountDinner = realBillPhoneCashCountDinner + realBillPhoneCardCountDinner - realBillTaPhoneDividePayCountDinner
    sumrealBillPhoneDinner = realBillPhoneCashDinner + realBillPhoneCardDinner
    # Row 7 T/A Online Dinner
    sumrealBillOnlineCountDinner = realBillOnlineCashCountDinner + \
        realBillOnlineCardCountDinner
    sumrealBillOnlineDinner = realBillOnlineCashDinner + realBillOnlineCardDinner
    # Row 8 Dine-in Dinner
    sumrealBillInCountDinner = realBillInCashCountDinner + realBillInCardCountDinner - realBillDineInDividePayCountDinner
    sumrealBillInDinner = realBillInCashDinner + realBillInCardDinner
    # Row 10 Column 4
    sumCash = realBillOnlineCashLunch + realBillPhoneCashLunch + realBillInCashLunch + realBillHomePhoneCashDinner + \
        realBillHomeOnlineCashDinner + realBillPhoneCashDinner + \
        realBillOnlineCashDinner + realBillInCashDinner
    # Row 10 Column 5
    sumCard = realBillOnlineCardLunch + realBillPhoneCardLunch + realBillInCardLunch + realBillHomePhoneCardDinner + \
        realBillHomeOnlineCardDinner + realBillPhoneCardDinner + \
        realBillOnlineCardDinner + realBillInCardDinner
    # Right Section
    totalBillDinner = intcomma(sumTotal - totalBillLunch)

    # * Delivery section
    # Sum all count both phone and online and
    sumrealBillHomeCountDinner = sumrealBillHomePhoneCountDinner + \
        sumrealBillHomeOnlineCountDinner
    totalSumCommissionAndOa = sum(
        detail.sum_commission_and_oa for detail in related_delivery_details)

    # * Other section
    sumTip = tipLunch + tipDinner
    sumWrongCredit = wrongCreditLunch + wrongCreditDinner
    totalOnlineCount = realBillOnlineCardCountLunch + realBillOnlineCashCountLunch + realBillOnlineCashCountDinner + \
        realBillOnlineCardCountDinner + realBillHomeOnlineCashCountDinner + \
        realBillHomeOnlineCardCountDinner
    totalOnlineAmount = realBillOnlineCardLunch + realBillOnlineCashLunch + realBillOnlineCashDinner +\
        realBillOnlineCardDinner + realBillHomeOnlineCashDinner + realBillHomeOnlineCardDinner

    # Disburse Section
    totalSumDisburse = sum(detail.price for detail in related_disburse_details)
    balanceAfterMinusExpense = sumCash - \
        totalSumCommissionAndOa - totalSumDisburse - sumTip

    imgLocation = GenerateImageWIthText(sumrealBillOnlineCount,sumrealBillOnline,realBillOnlineCashLunch,realBillOnlineCardLunch,sumrealBillPhoneCount,realBillPhoneLunch,realBillPhoneCashLunch,realBillPhoneCardLunch,sumrealBillInCount,sumrealBillIn,realBillInCashLunch,realBillInCardLunch,realBillHomePhoneCashDinner,realBillHomePhoneCardDinner,sumrealBillHomePhoneCountDinner,sumrealBillHomePhoneDinner,realBillHomeOnlineCashDinner,realBillHomeOnlineCardDinner,sumrealBillHomeOnlineCountDinner,sumrealBillHomeOnlineDinner,sumrealBillPhoneCountDinner,sumrealBillPhoneDinner,realBillPhoneCashDinner,realBillPhoneCardDinner,sumrealBillOnlineCountDinner,sumrealBillOnlineDinner,realBillOnlineCashDinner,realBillOnlineCardDinner,sumrealBillInCountDinner,sumrealBillInDinner,realBillInCashDinner,realBillInCardDinner,sumTotal,sumCash,sumCard,totalBillLunch,totalBillDinner,tipLunch,tipDinner,related_delivery_details,sumrealBillHomeCountDinner,totalSumCommissionAndOa,totalOnlineCount,totalOnlineAmount,day,dateForImage,related_disburse_details,totalSumDisburse,balanceAfterMinusExpense,wrongCreditLunch,wrongCreditDinner)

    context = {
        'date': date,
        'daily_report_id': daily_report_id,
        #! Lunch
        # Row 1 Ta Online Lunch
        'sumrealBillOnlineCount': sumrealBillOnlineCount,
        'sumrealBillOnline': sumrealBillOnline,
        'realBillOnlineCashLunch': realBillOnlineCashLunch,
        'realBillOnlineCardLunch': realBillOnlineCardLunch,
        # Row 2 Ta Phone Lunch
        'sumrealBillPhoneCount': sumrealBillPhoneCount,
        'sumrealBillPhone': realBillPhoneLunch,
        'realBillPhoneCashLunch': realBillPhoneCashLunch,
        'realBillPhoneCardLunch': realBillPhoneCardLunch,
        # Row 3 Dine-in Lunch
        'sumrealBillInCount': sumrealBillInCount,
        'sumrealBillIn': sumrealBillIn,
        'realBillInCashLunch': realBillInCashLunch,
        'realBillInCardLunch': realBillInCardLunch,
        # Row other
        'tipLunch': tipLunch,
        #! Dinner
        # Row 4 Home Phone
        'realBillHomePhoneCashDinner': realBillHomePhoneCashDinner,
        'realBillHomePhoneCardDinner': realBillHomePhoneCardDinner,
        'sumrealBillHomePhoneCountDinner': sumrealBillHomePhoneCountDinner,
        'sumrealBillHomePhoneDinner': sumrealBillHomePhoneDinner,
        # Row 5 Home Online
        'realBillHomeOnlineCashDinner': realBillHomeOnlineCashDinner,
        'realBillHomeOnlineCardDinner': realBillHomeOnlineCardDinner,
        'sumrealBillHomeOnlineCountDinner': sumrealBillHomeOnlineCountDinner,
        'sumrealBillHomeOnlineDinner': sumrealBillHomeOnlineDinner,
        # Row 6 T/A Phone Dinner
        'sumrealBillPhoneCountDinner': sumrealBillPhoneCountDinner,
        'sumrealBillPhoneDinner': sumrealBillPhoneDinner,
        'realBillPhoneCashDinner': realBillPhoneCashDinner,
        'realBillPhoneCardDinner': realBillPhoneCardDinner,
        # Row 7 T/A Online Dinner
        'sumrealBillOnlineCountDinner': sumrealBillOnlineCountDinner,
        'sumrealBillOnlineDinner': sumrealBillOnlineDinner,
        'realBillOnlineCashDinner': realBillOnlineCashDinner,
        'realBillOnlineCardDinner': realBillOnlineCardDinner,
        # Row 8 Dine-in Dinner
        'sumrealBillInCountDinner': sumrealBillInCountDinner,
        'sumrealBillInDinner': sumrealBillInDinner,
        'realBillInCashDinner': realBillInCashDinner,
        'realBillInCardDinner': realBillInCardDinner,
        # Row other
        'tipDinner': tipDinner,
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
        'totalSumDisburse': totalSumDisburse,

        #! Home section
        'related_delivery_details': related_delivery_details,
        'sumrealBillHomeCountDinner': sumrealBillHomeCountDinner,
        'totalSumCommissionAndOa': totalSumCommissionAndOa,

        #! Disburse Section
        'related_disburse_details': related_disburse_details,
        'balanceAfterMinusExpense': balanceAfterMinusExpense,

        # Image
        'imgLocation': imgLocation,
    }

    return render(request, 'keywordapp/report-image.html', context)
    # return render(request, 'keywordapp/dinner-report.html', context)


def HomeList(request, daily_report_id):

    daily_report = get_object_or_404(DailyReportModel, id=daily_report_id)
    date = daily_report.date
    bill_dinner_id = daily_report.bill_dinner_id
    bill_dinner = get_object_or_404(BillDinnerModel, id=bill_dinner_id)

    # You can also access the related DeliveryDetailModel instances from a DailyReportModel instance
    related_delivery_details = daily_report.bill_dinner.deliverydetailmodel_set.all()
    deliveryTotalCount = 0
    deliveryTotalCommissionAndOa = 0
    for detail in related_delivery_details:
        detail.sum_commission = detail.wage_per_home * (detail.real_bill_home_phone_cash_count + detail.real_bill_home_phone_card_count +
                                                        detail.real_bill_home_online_cash_count + detail.real_bill_home_online_card_count)
        detail.home_count = detail.real_bill_home_phone_cash_count + detail.real_bill_home_phone_card_count + \
            detail.real_bill_home_online_cash_count + \
            detail.real_bill_home_online_card_count
        detail.sum_commission_and_oa = (
            detail.real_bill_home_oa_count * detail.real_bill_home_oa_amount) + detail.sum_commission

        deliveryTotalCount += detail.home_count
        deliveryTotalCommissionAndOa += detail.sum_commission_and_oa

    context = {
        'date': date,
        'daily_report_id': daily_report_id,
        'bill_dinner': bill_dinner,
        'deliveryTotalCount': deliveryTotalCount,
        'deliveryTotalCommissionAndOa': deliveryTotalCommissionAndOa,
        'related_delivery_details': related_delivery_details,
    }
    return render(request, 'keywordapp/home-list.html', context)


def HomeInputQuick(request, daily_report_id, delivery_id):

    daily_object = get_object_or_404(DailyReportModel, id=daily_report_id)
    date = daily_object.date
    bill_dinner = daily_object.bill_dinner
    if delivery_id == 0:
        newDeliveryMan = DeliveryDetailModel.objects.create(
            bill_dinner=bill_dinner)
        newDeliveryManId = newDeliveryMan.id
        return redirect(reverse('home-input-quick', kwargs={'daily_report_id': daily_report_id, 'delivery_id': newDeliveryManId}))

    if request.method == 'POST':
        # Home
        realBillHomePhoneCashCount = request.POST.get(
            'real_bill_home_phone_cash_count')
        realBillHomePhoneCash = request.POST.get('real_bill_home_phone_cash')
        realBillHomePhoneCardCount = request.POST.get(
            'real_bill_home_phone_card_count')
        realBillHomePhoneCard = request.POST.get('real_bill_home_phone_card')
        realBillHomeOnlineCashCount = request.POST.get(
            'real_bill_home_online_cash_count')
        realBillHomeOnlineCash = request.POST.get('real_bill_home_online_cash')
        realBillHomeOnlineCardCount = request.POST.get(
            'real_bill_home_online_card_count')
        realBillHomeOnlineCard = request.POST.get('real_bill_home_online_card')

        realBillHomeOaCount = request.POST.get('real_bill_home_oa_count')
        realBillHomeOaAmount = request.POST.get('real_bill_home_oa_amount')
        deliveryName = request.POST.get('delivery_name')
        edcHomeCredit = request.POST.get('edc_home_credit')
        motoCredit = request.POST.get('moto_credit')
        wagePerHour = request.POST.get('wage_per_home')

        delivery_detail = get_object_or_404(
            DeliveryDetailModel, id=delivery_id)

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
        delivery_detail.edc_home_credit = edcHomeCredit
        delivery_detail.moto_credit = motoCredit

        delivery_detail.save()

        return redirect(reverse('home-input-detail', kwargs={'daily_report_id': daily_report_id, 'delivery_id': delivery_id}))

    delivery_detail = DeliveryDetailModel.objects.get(id=delivery_id)

    context = {
        'date': date,
        'daily_report_id': daily_report_id,
        'delivery_detail': delivery_detail,
    }
    return render(request, 'keywordapp/home-input-quick.html', context)


def HomeInputDetail(request, daily_report_id, delivery_id):

    daily_object = get_object_or_404(DailyReportModel, id=daily_report_id)
    date = daily_object.date
    delivery_detail = DeliveryDetailModel.objects.get(id=delivery_id)

    # Summary
    sumHomePhoneCount = delivery_detail.real_bill_home_phone_cash_count + \
        delivery_detail.real_bill_home_phone_card_count
    sumHomeOnlineCount = delivery_detail.real_bill_home_online_cash_count + \
        delivery_detail.real_bill_home_online_card_count
    sumHomeCount = delivery_detail.real_bill_home_phone_cash_count + delivery_detail.real_bill_home_phone_card_count + \
        delivery_detail.real_bill_home_online_cash_count + \
        delivery_detail.real_bill_home_online_card_count
    sumHomeCardAmount = delivery_detail.real_bill_home_phone_card + \
        delivery_detail.real_bill_home_online_card

    # Calculation
    sumHomeCommission = sumHomeCount * delivery_detail.wage_per_home
    sumHomeCommissionAndOa = sumHomeCommission + \
        delivery_detail.real_bill_home_oa_amount
    AddMotoToEdcCard = delivery_detail.edc_home_credit + delivery_detail.moto_credit

    # Comparation
    resultCheckEqual = "✅" if sumHomeCardAmount == AddMotoToEdcCard else "❌"

    context = {
        'date': date,
        'delivery_detail': delivery_detail,
        'daily_report_id': daily_report_id,
        'sumHomeCount': sumHomeCount,
        'sumHomePhoneCount': sumHomePhoneCount,
        'sumHomeOnlineCount': sumHomeOnlineCount,
        'sumHomeCommission': sumHomeCommission,
        'sumHomeCardAmount': sumHomeCardAmount,
        'sumHomeCommissionAndOa': sumHomeCommissionAndOa,
        'resultCheckEqual': resultCheckEqual,
        'AddMotoToEdcCard': AddMotoToEdcCard,
    }
    return render(request, 'keywordapp/home-input-detail.html', context)


def GetOnlineOrderData(request, daily_report_id, shift='dinner'):

    daily_report = get_object_or_404(DailyReportModel, id=daily_report_id)
    input_date = daily_report.date
    input_date = input_date.strftime('%b %d, %Y')

    options = webdriver.ChromeOptions()
    # Specify the path to your custom user data directory
    custom_user_data_dir = '/Users/chaperone/Library/Application Support/Google/Chrome/Default'
    options.add_argument(f'--user-data-dir={custom_user_data_dir}')

    # options.add_argument("--headless")
    #! PC
    # driver = webdriver.Chrome(options=options)
    #! MAC
    options.add_argument("start-maximized")
    # Replace with the actual path to the Chrome binary
    options.binary_location = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
    driver = webdriver.Chrome(
        "/Users/chaperone/Documents/GitHub/chromedriver", options=options)

    driver.get('https://gloriafood.com/')

    # Wait for Login button
    element_locator = (By.XPATH, '//*[@id="navbar"]/ul/li[4]/a')
    element = WaitForElement(driver, element_locator)
    if element:
        login_button = driver.find_element(
            By.XPATH, '//*[@id="navbar"]/ul/li[4]/a')
        login_button.click()
    else:
        driver.quit()

    # Wait for username and password block
    element_locator = (By.XPATH, '//*[@id="login-email"]')
    element = WaitForElement(driver, element_locator)
    if element:
        time.sleep(1)
        username = driver.find_element(By.XPATH, '//*[@id="login-email"]')
        username.send_keys("chain_shane@yahoo.com")
        password = driver.find_element(By.XPATH, '//*[@id="login-password"]')
        password.send_keys("bitesme1234")
        button_login = driver.find_element(
            By.XPATH, '//*[@id="login-form"]/div[5]/button')
        button_login.click()
    else:
        driver.quit()

    targetLinkText = "https://www.gloriafood.com/admin/?user_id=7961955&session_token=WEB_SESSION&acid=742458"
    targetLinkText2 = "https://www.gloriafood.com/admin2/app/company/dashboard/restaurants/list?acid=742458"

    while driver.current_url != targetLinkText or driver.current_url != targetLinkText2:
        time.sleep(0.5)
        if driver.current_url == targetLinkText or driver.current_url == targetLinkText2:
            driver.get(
                "https://www.gloriafood.com/admin2/app/restaurant/reports/listview/orders?acid=742459")
            break

    # Wait for data in table
    element_locator = (By.XPATH, "//tr[contains(@class, 'ng-star-inserted')]")
    element = WaitForElement(driver, element_locator, 60)
    if element:
        time.sleep(1)
        table_rows = driver.find_elements(
            By.XPATH, "//tr[contains(@class, 'ng-star-inserted')]")

        ScrapingOnlineData(table_rows, input_date, shift, daily_report_id)
    else:
        driver.quit()
    if shift == 'lunch':
        return redirect(reverse('lunch-input-detail', kwargs={'daily_report_id': daily_report_id}))
    elif shift == 'dinner':
        return redirect(reverse('dinner-input-detail', kwargs={'daily_report_id': daily_report_id}))
    elif shift == 'home':
        return redirect(reverse('home-list', kwargs={'daily_report_id': daily_report_id}))


def WaitForElement(driver, element_locator, wait_time=10):
    try:
        element = WebDriverWait(driver, wait_time).until(
            EC.presence_of_element_located(element_locator))
        return element
    except TimeoutException:
        return None


def ScrapingOnlineData(table_rows, input_date, shift, daily_report_id):

    daily_report = get_object_or_404(DailyReportModel, id=daily_report_id)
    bill_lunch_id = daily_report.bill_lunch_id
    bill_dinner_id = daily_report.bill_dinner_id

    total_type_delivery = 0
    total_type_pickup = 0
    delivery_cash_count = 0
    delivery_card_count = 0
    pickup_cash_count = 0
    pickup_card_count = 0
    delivery_cash_amount = 0
    delivery_card_amount = 0
    pickup_cash_amount = 0
    pickup_card_amount = 0

    for row in table_rows:
        # Get all child <td> elements within the row
        td_elements = row.find_elements(By.TAG_NAME, "td")
        try:
            date = td_elements[1].text
            time = date.split('\n')[0]
            getShiftFromTime = GetShift(time)
            lowerShift = getShiftFromTime.lower()
            date = date.split('\n')[1]
            if date == input_date:
                # Find shift from selected
                if shift == lowerShift:
                    type = td_elements[2].text
                    amount = td_elements[4].text
                    amount_decimal_format = Decimal(amount[0:5])
                    status = td_elements[5].text
                    payment_method = td_elements[6].text

                    if status == "Accepted":
                        if type == 'Delivery':
                            total_type_delivery += 1
                            if payment_method == "Cash":
                                delivery_cash_count += 1
                                delivery_cash_amount += amount_decimal_format
                            elif payment_method == "Card":
                                delivery_card_count += 1
                                delivery_card_amount += amount_decimal_format
                        elif type == 'Pickup':
                            total_type_pickup += 1
                            if payment_method == "Cash":
                                pickup_cash_count += 1
                                pickup_cash_amount += amount_decimal_format
                            elif payment_method == "Card":
                                pickup_card_count += 1
                                pickup_card_amount += amount_decimal_format
        except:
            pass

    if shift == "lunch":
        bill_lunch = get_object_or_404(BillLunchModel, id=bill_lunch_id)
        bill_lunch.real_bill_online_cash_count = pickup_cash_count
        bill_lunch.real_bill_online_card_count = pickup_card_count
        bill_lunch.real_bill_online_cash = pickup_cash_amount
        bill_lunch.real_bill_online_card = pickup_card_amount
        bill_lunch.save()
    elif shift == "dinner" or shift == "home":
        bill_dinner = get_object_or_404(BillDinnerModel, id=bill_dinner_id)
        bill_dinner.real_bill_online_cash_count = pickup_cash_count
        bill_dinner.real_bill_online_card_count = pickup_card_count
        bill_dinner.real_bill_online_cash = pickup_cash_amount
        bill_dinner.real_bill_online_card = pickup_card_amount
        bill_dinner.delivery_cash_count_in_online_system = delivery_cash_count
        bill_dinner.delivery_cash_amount_in_online_system = delivery_cash_amount
        bill_dinner.delivery_card_count_in_online_system = delivery_card_count
        bill_dinner.delivery_card_amount_in_online_system = delivery_card_amount
        bill_dinner.save()
    return 0


def GetShift(time_str):
    time_format = "%I:%M %p"
    lunch_start = datetime.datetime.strptime("11:00 AM", time_format).time()
    lunch_end = datetime.datetime.strptime("4:00 PM", time_format).time()
    dinner_start = datetime.datetime.strptime("4:30 PM", time_format).time()
    dinner_end = datetime.datetime.strptime("10:00 PM", time_format).time()

    time_obj = datetime.datetime.strptime(time_str, time_format).time()

    if lunch_start <= time_obj <= lunch_end:
        return "Lunch"
    elif dinner_start <= time_obj <= dinner_end:
        return "Dinner"
    else:
        return "Other Shift"


def DeleteDeliveryDetail(request, delivery_detail_id, daily_report_id):
    delivery_detail = get_object_or_404(
        DeliveryDetailModel, id=delivery_detail_id)
    delivery_detail.delete()
    return redirect(reverse('home-list', kwargs={'daily_report_id': daily_report_id}))


def DeleteDisburse(request, disburse_id, daily_report_id):
    disburse = get_object_or_404(DisburseModel, id=disburse_id)
    disburse.delete()
    return redirect(reverse('disburse-list', kwargs={'daily_report_id': daily_report_id}))

def GenerateImageWIthText(sumrealBillOnlineCount,sumrealBillOnline,realBillOnlineCashLunch,realBillOnlineCardLunch,sumrealBillPhoneCount,realBillPhoneLunch,realBillPhoneCashLunch,realBillPhoneCardLunch,sumrealBillInCount,sumrealBillIn,realBillInCashLunch,realBillInCardLunch,realBillHomePhoneCashDinner,realBillHomePhoneCardDinner,sumrealBillHomePhoneCountDinner,sumrealBillHomePhoneDinner,realBillHomeOnlineCashDinner,realBillHomeOnlineCardDinner,sumrealBillHomeOnlineCountDinner,sumrealBillHomeOnlineDinner,sumrealBillPhoneCountDinner,sumrealBillPhoneDinner,realBillPhoneCashDinner,realBillPhoneCardDinner,sumrealBillOnlineCountDinner,sumrealBillOnlineDinner,realBillOnlineCashDinner,realBillOnlineCardDinner,sumrealBillInCountDinner,sumrealBillInDinner,realBillInCashDinner,realBillInCardDinner,sumTotal,sumCash,sumCard,totalBillLunch,totalBillDinner,tipLunch,tipDinner,related_delivery_details,sumrealBillHomeCountDinner,totalSumCommissionAndOa,totalOnlineCount,totalOnlineAmount,day,dateForImage,related_disburse_details,totalSumDisburse,balanceAfterMinusExpense,wrongCreditLunch,wrongCreditDinner):

    path = os.getcwd()
    locationTemplate = os.path.join(path, 'static', 'img', 'template.jpg')

    # * ================= START :  SET FONT =================
    fontPath = os.path.join(path, 'static', 'fonts', 'kanit.ttf')
    fontThai = ImageFont.truetype(fontPath, 24)
    fontTotalShift = ImageFont.truetype(fontPath, 36)

# * ================= END :  SET FONT =================

    img = Image.open(locationTemplate)
    imgObj = ImageDraw.Draw(img)

    # * ================= START :  GET FONT COLOR =================
    # ? date text
    FontColor = (255, 255, 255)

    # * ================= END :  GET FONT COLOR =================
    # Row 1 Ta Online Lunch
    imgObj.text((60, 50), str(sumrealBillOnlineCount), font=fontThai, fill=FontColor) # Total Count
    imgObj.text((90, 50), str("TA Online"), font=fontThai, fill=FontColor) # Total Count
    imgObj.text((300, 50), str(sumrealBillOnline), font=fontThai, fill=FontColor) # Total Amount
    imgObj.text((430, 50), str(realBillOnlineCashLunch), font=fontThai, fill=FontColor) # Cash Amount
    imgObj.text((590, 50), str(realBillOnlineCardLunch), font=fontThai, fill=FontColor) # Card Amount
    # Row 2 Ta Phone Lunch
    imgObj.text((60, 130), str(sumrealBillPhoneCount), font=fontThai, fill=FontColor) # Total Count
    imgObj.text((300, 140), str(realBillPhoneLunch), font=fontThai, fill=FontColor) # Total Amount
    imgObj.text((430, 140), str(realBillPhoneCashLunch), font=fontThai, fill=FontColor) # Cash Amount
    imgObj.text((590, 140), str(realBillPhoneCardLunch), font=fontThai, fill=FontColor) # Card Amount
    # Row 3 Dine-in Lunch
    imgObj.text((60, 170), str(sumrealBillInCount), font=fontThai, fill=FontColor) # Total Count
    imgObj.text((300, 180), str(sumrealBillIn), font=fontThai, fill=FontColor) # Total Amount
    imgObj.text((430, 180), str(realBillInCashLunch), font=fontThai, fill=FontColor) # Cash Amount
    imgObj.text((590, 180), str(realBillInCardLunch), font=fontThai, fill=FontColor) # Card Amount
    # Row 4 Home Phone
    imgObj.text((60, 210), str(sumrealBillHomePhoneCountDinner), font=fontThai, fill=FontColor) # Total Count
    imgObj.text((300, 220), str(sumrealBillHomePhoneDinner), font=fontThai, fill=FontColor) # Total Amount
    imgObj.text((430, 220), str(realBillHomePhoneCashDinner), font=fontThai, fill=FontColor) # Cash Amount
    imgObj.text((590, 220), str(realBillHomePhoneCardDinner), font=fontThai, fill=FontColor) # Card Amount
    # Row 5 Home Online
    imgObj.text((60, 250), str(sumrealBillHomeOnlineCountDinner), font=fontThai, fill=FontColor) # Total Count
    imgObj.text((300, 260), str(sumrealBillHomeOnlineDinner), font=fontThai, fill=FontColor) # Total Amount
    imgObj.text((430, 260), str(realBillHomeOnlineCashDinner), font=fontThai, fill=FontColor) # Cash Amount
    imgObj.text((590, 260), str(realBillHomeOnlineCardDinner), font=fontThai, fill=FontColor) # Card Amount
    # Row 6 T/A Phone Dinner
    imgObj.text((60, 290), str(sumrealBillPhoneCountDinner), font=fontThai, fill=FontColor) # Total Count
    imgObj.text((300, 300), str(sumrealBillPhoneDinner), font=fontThai, fill=FontColor) # Total Amount
    imgObj.text((430, 300), str(realBillPhoneCashDinner), font=fontThai, fill=FontColor) # Cash Amount
    imgObj.text((590, 300), str(realBillPhoneCardDinner), font=fontThai, fill=FontColor) # Card Amount
    # Row 7 T/A Online Dinner
    imgObj.text((60, 330), str(sumrealBillOnlineCountDinner), font=fontThai, fill=FontColor) # Total Count
    imgObj.text((300, 340), str(sumrealBillOnlineDinner), font=fontThai, fill=FontColor) # Total Amount
    imgObj.text((430, 340), str(realBillOnlineCashDinner), font=fontThai, fill=FontColor) # Cash Amount
    imgObj.text((590, 340), str(realBillOnlineCardDinner), font=fontThai, fill=FontColor) # Card Amount
    # Row 8 Dine-in Dinner
    imgObj.text((60, 380), str(sumrealBillInCountDinner), font=fontThai, fill=FontColor) # Total Count
    imgObj.text((300, 380), str(sumrealBillInDinner), font=fontThai, fill=FontColor) # Total Amount
    imgObj.text((430, 380), str(realBillInCashDinner), font=fontThai, fill=FontColor) # Cash Amount
    imgObj.text((590, 380), str(realBillInCardDinner), font=fontThai, fill=FontColor) # Card Amount
    # Row 9 Total
    imgObj.text((300, 420), str(sumTotal), font=fontThai, fill=FontColor) # Total Amount
    addTransparentHighlight(img, str(sumTotal), (300, 420), fontTotalShift, 0.2,'orange')
    imgObj.text((430, 420), str(sumCash), font=fontThai, fill=FontColor) # Cash Amount
    addTransparentHighlight(img, str(sumCash), (430, 420), fontTotalShift, 0.2,'orange')
    imgObj.text((590, 420), str(sumCard), font=fontThai, fill=FontColor) # Card Amount
    addTransparentHighlight(img, str(sumCard), (590, 420), fontTotalShift, 0.2,'orange')
    # Right Column
    imgObj.text((760, 160), str(totalBillLunch), font=fontTotalShift, fill=FontColor) # Total Bill Lunch
    addTransparentHighlight(img, str(totalBillLunch), (760, 160), fontTotalShift, 0.2,'orange')

    imgObj.text((710, 300), str(totalBillDinner), font=fontTotalShift, fill=FontColor) # Total Bill Dinner
    addTransparentHighlight(img, str(totalBillDinner), (710, 300), fontTotalShift, 0.2,'orange')
    # Tip
    imgObj.text((590, 470), str('Tip Lunch '+str(tipLunch)), font=fontThai, fill=FontColor) # Tip Lunch
    addTransparentHighlight(img, str('Tip Lunch '), (590, 470), fontTotalShift, 0.5,'pink')
    imgObj.text((590, 500), str('Tip Dinner '+str(tipDinner)), font=fontThai, fill=FontColor) # Tip Dinner
    addTransparentHighlight(img, str('Tip Dinner '), (590, 500), fontTotalShift, 0.5,'pink')
    # Home Delivery
    homePosXHomeCount = 100
    homePosYHomeCount = 545
    homePosXShowOaCount = 120
    homePosYShowOaCount = 545
    homePosXSumCommission = 330
    homePosYSumCommission = 545
    homePosXShowOaAmount = 360
    homePosYShowOaAmount = 360
    homePosXDeliveryName = 420
    homePosYDeliveryName = 545

    for item in related_delivery_details:
        imgObj.text((homePosXHomeCount, homePosYHomeCount), str(item.home_count), font=fontThai, fill=FontColor) # Home Count
        imgObj.text((homePosXShowOaCount, homePosYShowOaCount), str(item.show_oa_count), font=fontThai, fill=FontColor) # Show OA Count
        imgObj.text((homePosXSumCommission, homePosYSumCommission), str(item.sum_commission), font=fontThai, fill=FontColor) # Sum Commission
        imgObj.text((homePosXShowOaAmount, homePosYShowOaAmount), str(item.show_oa_amount), font=fontThai, fill=FontColor) # Show OA Amount
        imgObj.text((homePosXDeliveryName, homePosYDeliveryName), str(item.delivery_name), font=fontThai, fill=FontColor) # Show OA Amount
        # Step position down
        homePosYHomeCount += 45
        homePosYShowOaCount += 45
        homePosYSumCommission += 45
        homePosYShowOaAmount += 45
        homePosYDeliveryName += 45
    
    imgObj.text((100, 670), str(sumrealBillHomeCountDinner)+'                      '+str(totalSumCommissionAndOa), font=fontThai, fill=FontColor) # Total Delivery
    addTransparentHighlight(img, str(sumrealBillHomeCountDinner)+'                   ', (100, 670), fontTotalShift, 0.2,'pink')

    # Total Online
    imgObj.text((690, 545), '('+str(totalOnlineCount)+') '+str(totalOnlineAmount), font=fontThai, fill=FontColor) # Total Online
    addTransparentHighlight(img,'  '+str(totalOnlineAmount), (690, 545), fontTotalShift, 0.2,'orange')

    # Wrong Credit
    imgObj.text((550, 700),'กดเครดิตขาด(เที่ยง) '+str(wrongCreditLunch), font=fontThai, fill=FontColor) # Wrong Credit Lunch
    addTransparentHighlight(img,'                     ', (550, 700), fontTotalShift, 0.2,'orange')
    imgObj.text((550, 730),'กดเครดิตขาด(เย็น) '+str(wrongCreditDinner), font=fontThai, fill=FontColor) # Wrong Credit Dinner
    addTransparentHighlight(img,'                     ', (550, 730), fontTotalShift, 0.2,'orange')
    # Dairy Record
    imgObj.text((1000, 90), str(day), font=fontThai, fill=FontColor) # Day
    imgObj.text((1000, 130), str(dateForImage), font=fontThai, fill=FontColor) # Date

    # Dairy Expense
    ExpensePosX = 950
    ExpensePosY = 380
    for item in related_disburse_details:
        imgObj.text((ExpensePosX, ExpensePosY), str(str(item.name)+'  '+str(item.price)), font=fontThai, fill=FontColor) # Expense
        # Step position down
        ExpensePosY += 40
    
    imgObj.text((980, 780), str(totalSumDisburse), font=fontTotalShift, fill=FontColor) # Total
    addTransparentHighlight(img,str(totalSumDisburse), (980, 780), fontTotalShift, 0.5,'pink')

    # Balance
    imgObj.text((350, 780), str(balanceAfterMinusExpense), font=fontTotalShift, fill=FontColor) # Balance
    addTransparentHighlight(img,str(balanceAfterMinusExpense), (350, 780), fontTotalShift, 0.2,'orange')

    locationSaved = path+'/static/img/result.jpg'
    img.save(locationSaved)
    imgLocation = '/static/img/result.jpg'

    return imgLocation

def addTransparentHighlight(image, text, text_position, font, opacity,color='orange'):
    # Create a new transparent image with the same size as the original image
    rect_img = Image.new('RGBA', image.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(rect_img)

    # Draw the text on the transparent image
    draw.text(text_position, text, font=font)

    # Calculate the size of the text
    text_width, text_height = draw.textsize(text, font=font)

    # Define the coordinates of the rectangle that will surround the text
    rect_x1, rect_y1 = text_position
    rect_x2, rect_y2 = text_position[0] + text_width, text_position[1] + text_height

    # Calculate the fill color with the specified opacity
    if color == 'orange':
        fill_color = (255,69,0, int(255 * opacity))
    elif color == 'pink':
        fill_color = (255,105,180, int(255 * opacity))

    # Draw a filled and transparent rectangle around the text
    draw.rectangle([rect_x1, rect_y1, rect_x2, rect_y2], outline=None, fill=fill_color)

    # Paste the transparent rectangle image over the original image
    image.paste(rect_img, (0, 0), rect_img)
    # path = os.getcwd()
    # locationSaved = path+'/static/img/result.jpg'
    # image.save(locationSaved)