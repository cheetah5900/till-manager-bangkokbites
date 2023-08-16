
# =============================== FOR PAGE KEYWORD MANAGER ===============================
# =============================== FOR PAGE KEYWORD MANAGER ===============================
# =============================== FOR PAGE KEYWORD MANAGER ===============================

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.conf import settings
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

# EMAIL
import imaplib
import ssl
import email
import time
from itertools import chain
import email
import imaplib

# Excel
import openpyxl
import pandas as pd
import shutil
import glob
import re
from bs4 import BeautifulSoup


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
        elif mode == 'home':
            return redirect(reverse('home-list', kwargs={'daily_report_id': daily_report.id}))
        elif mode == 'dinner':
            return redirect(reverse('dinner-input-quick', kwargs={'daily_report_id': daily_report.id}))
        elif mode == 'disburse':
            return redirect(reverse('disburse-list', kwargs={'daily_report_id': daily_report.id}))
        elif mode == 'scraping':
            return redirect(reverse('scraping', kwargs={'daily_report_id': daily_report.id}))
        elif mode == 'result':
            return redirect(reverse('dinner-report', kwargs={'daily_report_id': daily_report.id}))

    return render(request, 'keywordapp/index.html', context)

# ************************************************************************************************ START : DISBURSE ************************************************************************************************


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
# ************************************************************************************************ END : DISBURSE ************************************************************************************************
# ************************************************************************************************ START : LUNCH ************************************************************************************************


def LunchInputQuick(request, daily_report_id):

    daily_report = get_object_or_404(DailyReportModel, id=daily_report_id)
    date = daily_report.date
    bill_lunch_id = daily_report.bill_lunch.id

    bill_lunch = BillLunchModel.objects.get(id=bill_lunch_id)

    if request.method == 'POST':
        edcInCredit = request.POST.get('edc_in_credit')
        tipCredit = request.POST.get('tip_credit')
        wrongCredit = request.POST.get('wrong_credit')

        billOnlineCashCount = request.POST.get('bill_online_cash_count')
        billOnlineCash = request.POST.get('bill_online_cash')
        billOnlineCardCount = request.POST.get('bill_online_card_count')
        billOnlineCard = request.POST.get('bill_online_card')

        # Online
        bill_lunch = get_object_or_404(BillLunchModel, id=bill_lunch_id)
        bill_lunch.edc_in_credit = edcInCredit
        bill_lunch.tip_credit = tipCredit
        bill_lunch.wrong_credit = wrongCredit
        bill_lunch.bill_online_cash_count = billOnlineCashCount
        bill_lunch.bill_online_cash = billOnlineCash
        bill_lunch.bill_online_card_count = billOnlineCardCount
        bill_lunch.bill_online_card = billOnlineCard

        # Save the updated object
        bill_lunch.save()

        return redirect(reverse('lunch-report', kwargs={'daily_report_id': daily_report_id}))

    return render(request, 'keywordapp/lunch-input-quick.html', context={'date': date, 'bill_lunch': bill_lunch, 'daily_report_id': daily_report_id})


def LunchReport(request, daily_report_id):

    daily_report = get_object_or_404(DailyReportModel, id=daily_report_id)
    # Retrieve other related models or fields if needed

    date = daily_report.date
    bill_lunch_id = daily_report.bill_lunch.id

    bill_lunch = BillLunchModel.objects.get(id=bill_lunch_id)

    # * TA Phone
    realBillPhoneCash = bill_lunch.pos_ta_bill_phone_cash
    realBillPhoneCashCount = bill_lunch.pos_ta_bill_phone_cash_count
    realBillPhoneCard = bill_lunch.pos_ta_bill_phone_card
    realBillPhoneCardCount = bill_lunch.pos_ta_bill_phone_card_count

    posTaPhoneTotalBillCount = bill_lunch.pos_ta_phone_total_bill_count
    resultCompareTotalTaPhoneCount = (
        realBillPhoneCashCount + realBillPhoneCardCount) - posTaPhoneTotalBillCount

    # * POS Dine-in
    realBillInCash = bill_lunch.pos_in_bill_cash
    realBillInCashCount = bill_lunch.pos_in_bill_cash_count
    realBillInCard = bill_lunch.pos_in_bill_card
    realBillInCardCount = bill_lunch.pos_in_bill_card_count
    edcInCredit = bill_lunch.edc_in_credit

    posDineInTotalBillCount = bill_lunch.pos_dine_in_total_bill_count
    resultCompareTotalDineInCount = (
        realBillInCashCount + realBillInCardCount) - posDineInTotalBillCount

    # TA Online
    realBillOnlineCash = bill_lunch.bill_online_cash
    realBillOnlineCashCount = bill_lunch.bill_online_cash_count
    realBillOnlineCard = bill_lunch.bill_online_card
    realBillOnlineCardCount = bill_lunch.bill_online_card_count

    tipCredit = bill_lunch.tip_credit
    wrongCredit = bill_lunch.wrong_credit

    # summary
    sumBillPhoneCard = realBillPhoneCard + realBillInCard + realBillOnlineCard
    addTipToSum = sumBillPhoneCard + tipCredit
    addWrongCreditToEdcLunch = edcInCredit + wrongCredit
    resultCheckEqual = "✅" if addTipToSum == addWrongCreditToEdcLunch else "❌"

    # Summary
    # Row 1 TA Online
    sumrealBillOnlineCount = realBillOnlineCashCount + realBillOnlineCardCount
    sumrealBillOnline = realBillOnlineCash + realBillOnlineCard
    # Row 2 TA Phone Lunch
    sumrealBillPhoneCount = realBillPhoneCashCount + \
        realBillPhoneCardCount - resultCompareTotalTaPhoneCount
    sumrealBillPhone = realBillPhoneCash + realBillPhoneCard
    # Row 3 Dine-in Lunch
    sumrealBillInCount = realBillInCashCount + \
        realBillInCardCount - resultCompareTotalDineInCount
    sumrealBillIn = realBillInCash + realBillInCard
    # Summary all Lunch
    totalBillLunch = sumrealBillPhone + sumrealBillIn + sumrealBillOnline

    day = date.strftime("%A")
    dateForImage = date.strftime("%d / %m / %y")
    imgLocation = GenerateImageWIthText(sumrealBillOnlineCount, sumrealBillOnline, realBillOnlineCash, realBillOnlineCard, sumrealBillPhoneCount, sumrealBillPhone, realBillPhoneCash, realBillPhoneCard, sumrealBillInCount, sumrealBillIn, realBillInCash, realBillInCard, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, totalBillLunch, 0, tipCredit, 0, 0, 0, 0, 0, 0, day, dateForImage, 0, 0, 0, wrongCredit, 0)

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
        'resultCheckEqual': resultCheckEqual,
        'addTipToSum': addTipToSum,
        'addWrongCreditToEdcLunch': addWrongCreditToEdcLunch,
        'imgLocation': imgLocation,
    }
    return render(request, 'keywordapp/lunch-report.html', context)
# ************************************************************************************************ END : LUNCH ************************************************************************************************
# ************************************************************************************************ START : DINNER ************************************************************************************************


def DinnerInputQuick(request, daily_report_id):

    daily_object = get_object_or_404(DailyReportModel, id=daily_report_id)
    date = daily_object.date
    bill_dinner_id = daily_object.bill_dinner.id

    bill_dinner = BillDinnerModel.objects.get(id=bill_dinner_id)

    if request.method == 'POST':
        realBillOnlineCard = request.POST.get('bill_online_card')
        edcInCredit = request.POST.get('edc_in_credit')
        tipCredit = request.POST.get('tip_credit')
        wrongCredit = request.POST.get('wrong_credit')
        # Online
        realBillOnlineCash = request.POST.get('bill_online_cash')
        realBillOnlineCashCount = request.POST.get(
            'bill_online_cash_count')
        realBillOnlineCard = request.POST.get('bill_online_card')
        realBillOnlineCardCount = request.POST.get(
            'bill_online_card_count')

        bill_dinner = get_object_or_404(BillDinnerModel, id=bill_dinner_id)
        bill_dinner.bill_online_card = realBillOnlineCard
        bill_dinner.wrong_credit = wrongCredit
        bill_dinner.tip_credit = tipCredit
        bill_dinner.edc_in_credit = edcInCredit

        # TA Online
        bill_dinner.bill_online_cash_count = realBillOnlineCashCount
        bill_dinner.bill_online_cash = realBillOnlineCash
        bill_dinner.bill_online_card_count = realBillOnlineCardCount
        bill_dinner.bill_online_card = realBillOnlineCard

        # Save the updated object
        bill_dinner.save()

        return redirect(reverse('dinner-report', kwargs={'daily_report_id': daily_report_id}))

    return render(request, 'keywordapp/dinner-input-quick.html', context={'date': date, 'bill_dinner': bill_dinner, 'daily_report_id': daily_report_id})


def DinnerReport(request, daily_report_id):

    daily_report = get_object_or_404(DailyReportModel, id=daily_report_id)
    bill_dinner_id = daily_report.bill_dinner.id
    bill_dinner = BillDinnerModel.objects.get(id=bill_dinner_id)
    related_delivery_details = daily_report.bill_dinner.deliverydetailmodel_set.all()

    date = daily_report.date
    day = date.strftime("%A")
    dateForImage = date.strftime("%d / %m / %y")

    bill_lunch_id = daily_report.bill_lunch.id

    # * Lunch Data
    bill_lunch = BillLunchModel.objects.get(id=bill_lunch_id)
    realBillPhoneCashLunch = bill_lunch.pos_ta_bill_phone_cash
    realBillPhoneCashCountLunch = bill_lunch.pos_ta_bill_phone_cash_count
    realBillPhoneCardLunch = bill_lunch.pos_ta_bill_phone_card
    realBillPhoneCardCountLunch = bill_lunch.pos_ta_bill_phone_card_count
    realBillOnlineCashLunch = bill_lunch.bill_online_cash
    realBillOnlineCashCountLunch = bill_lunch.bill_online_cash_count
    realBillOnlineCardLunch = bill_lunch.bill_online_card
    realBillOnlineCardCountLunch = bill_lunch.bill_online_card_count
    realBillInCashLunch = bill_lunch.pos_in_bill_cash
    realBillInCashCountLunch = bill_lunch.pos_in_bill_cash_count
    realBillInCardLunch = bill_lunch.pos_in_bill_card
    realBillInCardCountLunch = bill_lunch.pos_in_bill_card_count
    tipLunch = bill_lunch.tip_credit
    edcInCreditLunch = bill_lunch.edc_in_credit
    wrongCreditLunch = bill_lunch.wrong_credit

    posTaPhoneTotalBillCount = bill_lunch.pos_ta_phone_total_bill_count
    resultCompareTotalTaPhoneCount = (
        realBillPhoneCashCountLunch + realBillPhoneCardCountLunch) - posTaPhoneTotalBillCount

    posDineInTotalBillCount = bill_lunch.pos_dine_in_total_bill_count
    resultCompareTotalDineInCount = (
        realBillInCashCountLunch + realBillInCardCountLunch) - posDineInTotalBillCount

    # * Dinner Data
    realBillPhoneCashDinner = bill_dinner.pos_ta_bill_phone_cash
    realBillPhoneCashCountDinner = bill_dinner.pos_ta_bill_phone_cash_count
    realBillPhoneCardDinner = bill_dinner.pos_ta_bill_phone_card
    realBillPhoneCardCountDinner = bill_dinner.pos_ta_bill_phone_card_count
    realBillOnlineCashDinner = bill_dinner.bill_online_cash
    realBillOnlineCashCountDinner = bill_dinner.bill_online_cash_count
    realBillOnlineCardDinner = bill_dinner.bill_online_card
    realBillOnlineCardCountDinner = bill_dinner.bill_online_card_count
    realBillInCashDinner = bill_dinner.pos_in_bill_cash
    realBillInCashCountDinner = bill_dinner.pos_in_bill_cash_count
    realBillInCardDinner = bill_dinner.pos_in_bill_card
    realBillInCardCountDinner = bill_dinner.pos_in_bill_card_count
    tipDinner = bill_dinner.tip_credit
    wrongCreditDinner = bill_dinner.wrong_credit

    posTaPhoneTotalBillCount = bill_dinner.pos_ta_phone_total_bill_count

    posDineInTotalBillCount = bill_dinner.pos_dine_in_total_bill_count
    resultCompareTotalDineInCountDinner = (
        realBillInCashCountDinner + realBillInCardCountDinner) - posDineInTotalBillCount

    # * Delivery Section
    # Access the related DeliveryDetailModel instances using the foreign key relationship
    related_delivery_details = daily_report.bill_dinner.deliverydetailmodel_set.all()

    # * Disburse Section
    related_disburse_details = daily_report.bill_dinner.disbursemodel_set.all()

    # Summarize the number of delivery man
    for detail in related_delivery_details:
        detail.sum_commission = int(detail.wage_per_home * (detail.bill_home_phone_cash_count +
                                    detail.bill_home_phone_card_count + detail.bill_home_online_cash_count + detail.bill_home_online_card_count))
        detail.home_count = detail.bill_home_phone_cash_count + detail.bill_home_phone_card_count + \
            detail.bill_home_online_cash_count + \
            detail.bill_home_online_card_count
        detail.sum_commission_and_oa = int(
            detail.bill_home_oa_amount + detail.sum_commission)
        if detail.bill_home_oa_count > 0:
            detail.show_oa_count = " + " + \
                str(detail.bill_home_oa_count)+" OA"
        else:
            detail.show_oa_count = ''
        if detail.bill_home_oa_amount > 0:
            detail.show_oa_amount = " + " + \
                str(int(detail.bill_home_oa_amount))
        else:
            detail.show_oa_amount = ''

    # sum all without separating delivery man
    realBillHomePhoneCashCountDinner = sum(
        detail.bill_home_phone_cash_count for detail in related_delivery_details)
    realBillHomePhoneCashDinner = sum(
        detail.bill_home_phone_cash for detail in related_delivery_details)
    realBillHomePhoneCardCountDinner = sum(
        detail.bill_home_phone_card_count for detail in related_delivery_details)
    realBillHomePhoneCardDinner = sum(
        detail.bill_home_phone_card for detail in related_delivery_details)
    realBillHomeOnlineCashCountDinner = sum(
        detail.bill_home_online_cash_count for detail in related_delivery_details)
    realBillHomeOnlineCashDinner = sum(
        detail.bill_home_online_cash for detail in related_delivery_details)
    realBillHomeOnlineCardCountDinner = sum(
        detail.bill_home_online_card_count for detail in related_delivery_details)
    realBillHomeOnlineCardDinner = sum(
        detail.bill_home_online_card for detail in related_delivery_details)

    countCashHomePhone = 0
    sumCashHomePhone = 0
    countCardHomePhone = 0
    sumCardHomePhone = 0
    for item in related_delivery_details:
        countCashHomePhone += item.bill_home_phone_cash_count
        sumCashHomePhone += item.bill_home_phone_cash
        countCardHomePhone += item.bill_home_phone_card_count
        sumCardHomePhone += item.bill_home_phone_card
    countAllHomePhone = countCashHomePhone + countCardHomePhone
    sumAllHomePhone = sumCashHomePhone + sumCardHomePhone
    # ? Summary
    # * Report Section
    # Row 1 Ta Online Lunch
    totalBillLunch = realBillPhoneCashLunch + realBillPhoneCardLunch + realBillInCashLunch + \
        realBillInCardLunch + realBillOnlineCashLunch + realBillOnlineCardLunch
    sumrealBillOnlineCount = realBillOnlineCashCountLunch + realBillOnlineCardCountLunch
    sumrealBillOnline = realBillOnlineCashLunch + realBillOnlineCardLunch
    # Row 2 Ta Phone Lunch
    sumrealBillPhoneCount = realBillPhoneCashCountLunch + \
        realBillPhoneCardCountLunch - resultCompareTotalTaPhoneCount
    realBillPhoneLunch = realBillPhoneCashLunch + realBillPhoneCardLunch
    # Row 3 Dine-in Lunch
    sumrealBillInCount = realBillInCashCountLunch + \
        realBillInCardCountLunch - resultCompareTotalDineInCount
    sumrealBillIn = realBillInCashLunch + realBillInCardLunch
    # Row 4
    sumrealBillHomePhoneDinner = realBillHomePhoneCashDinner + realBillHomePhoneCardDinner
    # Row 4 Home Phone
    sumrealBillHomePhoneCountDinner = realBillHomePhoneCashCountDinner + \
        realBillHomePhoneCardCountDinner
    # Row 5 Home Online
    sumrealBillHomeOnlineCountDinner = realBillHomeOnlineCashCountDinner + \
        realBillHomeOnlineCardCountDinner
    sumrealBillHomeOnlineDinner = realBillHomeOnlineCashDinner + \
        realBillHomeOnlineCardDinner
    # Row 6 T/A Phone Dinner
    sumrealBillPhoneCountDinner = realBillPhoneCashCountDinner + \
        realBillPhoneCardCountDinner - countAllHomePhone
    sumrealBillPhoneDinner = realBillPhoneCashDinner + \
        realBillPhoneCardDinner - sumAllHomePhone
    realBillPhoneCashDinnerMinusHomePhone = realBillPhoneCashDinner - sumCashHomePhone
    realBillPhoneCardDinnerMinusHomePhone = realBillPhoneCardDinner - sumCardHomePhone
    # Row 7 T/A Online Dinner
    sumrealBillOnlineCountDinner = realBillOnlineCashCountDinner + \
        realBillOnlineCardCountDinner
    sumrealBillOnlineDinner = realBillOnlineCashDinner + realBillOnlineCardDinner
    # Row 8 Dine-in Dinner
    sumrealBillInCountDinner = realBillInCashCountDinner + \
        realBillInCardCountDinner - resultCompareTotalDineInCountDinner
    sumrealBillInDinner = realBillInCashDinner + realBillInCardDinner
    # Row 10 Column 4
    sumCash = realBillOnlineCashLunch + realBillPhoneCashLunch + realBillInCashLunch + realBillHomePhoneCashDinner + \
        realBillHomeOnlineCashDinner + realBillPhoneCashDinnerMinusHomePhone + \
        realBillOnlineCashDinner + realBillInCashDinner
    # Row 10 Column 5
    sumCard = realBillOnlineCardLunch + realBillPhoneCardLunch + realBillInCardLunch + realBillHomePhoneCardDinner + \
        realBillHomeOnlineCardDinner + realBillPhoneCardDinnerMinusHomePhone + \
        realBillOnlineCardDinner + realBillInCardDinner
    # Row 10
    sumTotal = sumCash + sumCard
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
    totalOnlineCount = realBillOnlineCardCountLunch + realBillOnlineCashCountLunch + realBillOnlineCashCountDinner + \
        realBillOnlineCardCountDinner + realBillHomeOnlineCashCountDinner + \
        realBillHomeOnlineCardCountDinner
    totalOnlineAmount = realBillOnlineCardLunch + realBillOnlineCashLunch + realBillOnlineCashDinner +\
        realBillOnlineCardDinner + realBillHomeOnlineCashDinner + realBillHomeOnlineCardDinner

    # * Disburse Section
    totalSumDisburse = sum(detail.price for detail in related_disburse_details)
    balanceAfterMinusExpense = sumCash - \
        totalSumCommissionAndOa - totalSumDisburse - sumTip
    imgLocation = GenerateImageWIthText(sumrealBillOnlineCount, sumrealBillOnline, realBillOnlineCashLunch, realBillOnlineCardLunch, sumrealBillPhoneCount, realBillPhoneLunch, realBillPhoneCashLunch, realBillPhoneCardLunch, sumrealBillInCount, sumrealBillIn, realBillInCashLunch, realBillInCardLunch, realBillHomePhoneCashDinner, realBillHomePhoneCardDinner, sumrealBillHomePhoneCountDinner, sumrealBillHomePhoneDinner, realBillHomeOnlineCashDinner, realBillHomeOnlineCardDinner, sumrealBillHomeOnlineCountDinner, sumrealBillHomeOnlineDinner, sumrealBillPhoneCountDinner, sumrealBillPhoneDinner,
                                        realBillPhoneCashDinnerMinusHomePhone, realBillPhoneCardDinnerMinusHomePhone, sumrealBillOnlineCountDinner, sumrealBillOnlineDinner, realBillOnlineCashDinner, realBillOnlineCardDinner, sumrealBillInCountDinner, sumrealBillInDinner, realBillInCashDinner, realBillInCardDinner, sumTotal, sumCash, sumCard, totalBillLunch, totalBillDinner, tipLunch, tipDinner, related_delivery_details, sumrealBillHomeCountDinner, totalSumCommissionAndOa, totalOnlineCount, totalOnlineAmount, day, dateForImage, related_disburse_details, totalSumDisburse, balanceAfterMinusExpense, wrongCreditLunch, wrongCreditDinner)

    # * Summary for Comparation section

    # Access the related DeliveryDetailModel instances using the foreign key relationship
    related_delivery_details = daily_report.bill_dinner.deliverydetailmodel_set.all()

    # Calculate the sum of the bill_home_oa_amount attribute for all DeliveryDetailModel instances
    realBillHomePhoneCard = sum(
        detail.bill_home_phone_card for detail in related_delivery_details)
    realBillHomeOnlineCard = sum(
        detail.bill_home_online_card for detail in related_delivery_details)
    sumEdcHomeCard = sum(
        detail.edc_home_credit for detail in related_delivery_details)
    sumEdcMotoCard = sum(
        detail.moto_credit for detail in related_delivery_details)

    # Minus Home Phone Out From POS TA
    edcInMotoCredit = sum(
        detail.moto_credit for detail in related_delivery_details)
    minusHomePhoneOutFromPosTa = bill_dinner.pos_ta_bill_phone_card - realBillHomePhoneCard
    totalBillCardForCompareWithEdcDineIn = minusHomePhoneOutFromPosTa + bill_dinner.pos_in_bill_card + \
        bill_dinner.bill_online_card + bill_dinner.tip_credit + \
        edcInMotoCredit + bill_lunch.edc_in_credit

    #! The reason use only dinner because it is different shift from lunch shift.
    addWrongCreditToEdcDineIn = bill_dinner.edc_in_credit + wrongCreditDinner

    sumBillHomeCard = realBillHomePhoneCard + realBillHomeOnlineCard
    minusMotoCreditFromSumBillHomeCard = sumBillHomeCard - edcInMotoCredit

    resultCheckEqual1 = "✅" if totalBillCardForCompareWithEdcDineIn == addWrongCreditToEdcDineIn else "❌"
    resultCheckEqual2 = "✅" if minusMotoCreditFromSumBillHomeCard == sumEdcHomeCard else "❌"

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
        'edcInCreditLunch': edcInCreditLunch,
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
        'wrongCreditDinner': wrongCreditDinner,
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

        #! Comparation
        'bill_dinner': bill_dinner,
        'totalBillCardForCompareWithEdcDineIn': totalBillCardForCompareWithEdcDineIn,
        'minusHomePhoneOutFromPosTa': minusHomePhoneOutFromPosTa,
        'resultCheckEqual1': resultCheckEqual1,
        'resultCheckEqual2': resultCheckEqual2,
        'edcInCredit': bill_dinner.edc_in_credit,
        'edcInCreditLunch': bill_lunch.edc_in_credit,
        'edcInMotoCredit': edcInMotoCredit,
        'addWrongCreditToEdcDineIn': addWrongCreditToEdcDineIn,
        # Home
        'realBillHomePhoneCard': realBillHomePhoneCard,
        'realBillHomeOnlineCard': realBillHomeOnlineCard,
        'sumBillHomeCard': sumBillHomeCard,
        'minusMotoCreditFromSumBillHomeCard': minusMotoCreditFromSumBillHomeCard,
        'sumEdcHomeCard': sumEdcHomeCard,
        'sumEdcMotoCard': sumEdcMotoCard,
        'sumEdcMotoCard': sumEdcMotoCard,

    }

    return render(request, 'keywordapp/report-image.html', context)
# ************************************************************************************************ END : DINNER ************************************************************************************************
# ************************************************************************************************ START : HOME ************************************************************************************************


def HomeList(request, daily_report_id):

    daily_report = get_object_or_404(DailyReportModel, id=daily_report_id)
    date = daily_report.date
    bill_dinner_id = daily_report.bill_dinner_id
    bill_dinner = get_object_or_404(BillDinnerModel, id=bill_dinner_id)

    # You can also access the related DeliveryDetailModel instances from a DailyReportModel instance
    related_delivery_details = daily_report.bill_dinner.deliverydetailmodel_set.all()
    sumOnlineCashCount = 0
    sumOnlineCardCount = 0
    sumOnlineCash = 0
    sumOnlineCard = 0
    for detail in related_delivery_details:
        detail.sum_commission = detail.wage_per_home * (detail.bill_home_phone_cash_count + detail.bill_home_phone_card_count +
                                                        detail.bill_home_online_cash_count + detail.bill_home_online_card_count)
        detail.home_count = detail.bill_home_phone_cash_count + detail.bill_home_phone_card_count + \
            detail.bill_home_online_cash_count + \
            detail.bill_home_online_card_count
        detail.sum_commission_and_oa = detail.bill_home_oa_amount + detail.sum_commission

        sumOnlineCashCount += detail.bill_home_online_cash_count
        sumOnlineCardCount += detail.bill_home_online_card_count
        sumOnlineCash += detail.bill_home_online_cash
        sumOnlineCard += detail.bill_home_online_card

    context = {
        'date': date,
        'daily_report_id': daily_report_id,
        'bill_dinner': bill_dinner,
        'related_delivery_details': related_delivery_details,
        'sumOnlineCashCount': sumOnlineCashCount,
        'sumOnlineCardCount': sumOnlineCardCount,
        'sumOnlineCash': sumOnlineCash,
        'sumOnlineCard': sumOnlineCard,
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
            'bill_home_phone_cash_count')
        realBillHomePhoneCash = request.POST.get('bill_home_phone_cash')
        realBillHomePhoneCardCount = request.POST.get(
            'bill_home_phone_card_count')
        realBillHomePhoneCard = request.POST.get('bill_home_phone_card')
        realBillHomeOnlineCashCount = request.POST.get(
            'bill_home_online_cash_count')
        realBillHomeOnlineCash = request.POST.get('bill_home_online_cash')
        realBillHomeOnlineCardCount = request.POST.get(
            'bill_home_online_card_count')
        realBillHomeOnlineCard = request.POST.get('bill_home_online_card')

        realBillHomeOaCount = request.POST.get('bill_home_oa_count')
        realBillHomeOaAmount = request.POST.get('bill_home_oa_amount')
        deliveryName = request.POST.get('delivery_name')
        edcHomeCredit = request.POST.get('edc_home_credit')
        motoCredit = request.POST.get('moto_credit')
        wagePerHour = request.POST.get('wage_per_home')

        delivery_detail = get_object_or_404(
            DeliveryDetailModel, id=delivery_id)

        # Home  Phone
        delivery_detail.bill_home_phone_cash_count = realBillHomePhoneCashCount
        delivery_detail.bill_home_phone_cash = realBillHomePhoneCash
        delivery_detail.bill_home_phone_card_count = realBillHomePhoneCardCount
        delivery_detail.bill_home_phone_card = realBillHomePhoneCard
        # Home  Online
        delivery_detail.bill_home_online_cash_count = realBillHomeOnlineCashCount
        delivery_detail.bill_home_online_cash = realBillHomeOnlineCash
        delivery_detail.bill_home_online_card_count = realBillHomeOnlineCardCount
        delivery_detail.bill_home_online_card = realBillHomeOnlineCard
        # OA
        delivery_detail.bill_home_oa_count = realBillHomeOaCount
        delivery_detail.bill_home_oa_amount = realBillHomeOaAmount
        # Delivery man
        delivery_detail.delivery_name = deliveryName
        delivery_detail.wage_per_home = wagePerHour
        delivery_detail.edc_home_credit = edcHomeCredit
        delivery_detail.moto_credit = motoCredit

        delivery_detail.save()

        return redirect(reverse('home-report', kwargs={'daily_report_id': daily_report_id, 'delivery_id': delivery_id}))

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
    sumHomePhoneCount = delivery_detail.bill_home_phone_cash_count + \
        delivery_detail.bill_home_phone_card_count
    sumHomeOnlineCount = delivery_detail.bill_home_online_cash_count + \
        delivery_detail.bill_home_online_card_count
    sumHomeCount = delivery_detail.bill_home_phone_cash_count + delivery_detail.bill_home_phone_card_count + \
        delivery_detail.bill_home_online_cash_count + \
        delivery_detail.bill_home_online_card_count
    sumHomeCardAmount = delivery_detail.bill_home_phone_card + \
        delivery_detail.bill_home_online_card

    # Calculation
    sumHomeCommission = sumHomeCount * delivery_detail.wage_per_home
    sumHomeCommissionAndOa = sumHomeCommission + \
        delivery_detail.bill_home_oa_amount
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
    return render(request, 'keywordapp/home-report.html', context)


def DeleteDeliveryDetail(request, delivery_detail_id, daily_report_id):
    delivery_detail = get_object_or_404(
        DeliveryDetailModel, id=delivery_detail_id)
    delivery_detail.delete()
    return redirect(reverse('home-list', kwargs={'daily_report_id': daily_report_id}))

# ************************************************************************************************ END : HOME ************************************************************************************************
# ************************************************************************************************ START : ONLINE ************************************************************************************************


def GetOnlineOrderData(request, daily_report_id):

    daily_report = get_object_or_404(DailyReportModel, id=daily_report_id)
    input_date = daily_report.date
    input_date = input_date.strftime('%b %d, %Y')

    options = webdriver.ChromeOptions()

    # options.add_argument("--headless")
    options.add_argument("start-maximized")

    if settings.PC_OR_MAC == "PC":
        custom_user_data_dir = r'C:\Users\cheet\AppData\Local\Google\Chrome\User Data\Default'
        options.add_argument(f'--user-data-dir={custom_user_data_dir}')
        driver = webdriver.Chrome(options=options)
    elif settings.PC_OR_MAC == "MAC":
        # Specify the path to your custom user data directory
        custom_user_data_dir = '/Users/chaperone/Library/Application Support/Google/Chrome/Default'
        options.add_argument(f'--user-data-dir={custom_user_data_dir}')
        # Replace with the actual path to the Chrome binary
        options.binary_location = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
        driver = webdriver.Chrome(
            "/Users/chaperone/Documents/GitHub/chromedriver", options=options)

    # driver.get('https://gloriafood.com/')

    driver.get(
        "https://www.gloriafood.com/admin2/app/restaurant/reports/listview/orders?acid=742459")

    # # Wait for Login button
    # element_locator = (By.XPATH, '//*[@id="navbar"]/ul/li[4]/a')
    # element = WaitForElement(driver, element_locator)
    # if element:
    #     login_button = driver.find_element(
    #         By.XPATH, '//*[@id="navbar"]/ul/li[4]/a')
    #     login_button.click()
    # else:
    #     driver.quit()

    # # Wait for username and password block
    # element_locator = (By.XPATH, '//*[@id="login-email"]')
    # element = WaitForElement(driver, element_locator)
    # if element:
    #     time.sleep(1)
    #     username = driver.find_element(By.XPATH, '//*[@id="login-email"]')
    #     username.send_keys("chain_shane@yahoo.com")
    #     password = driver.find_element(By.XPATH, '//*[@id="login-password"]')
    #     password.send_keys("bitesme1234")
    #     button_login = driver.find_element(
    #         By.XPATH, '//*[@id="login-form"]/div[5]/button')
    #     button_login.click()
    # else:
    #     driver.quit()

    # targetLinkText = "https://www.gloriafood.com/admin/?user_id=7961955&session_token=WEB_SESSION&acid=742458"
    # targetLinkText2 = "https://www.gloriafood.com/admin2/app/company/dashboard/restaurants/list?acid=742458"

    # while driver.current_url != targetLinkText or driver.current_url != targetLinkText2:
    #     time.sleep(0.5)
    #     if driver.current_url == targetLinkText or driver.current_url == targetLinkText2:
    #         driver.get(
    #             "https://www.gloriafood.com/admin2/app/restaurant/reports/listview/orders?acid=742459")
    #         break

    # Wait for data in table
    element_locator = (By.XPATH, "//tr[contains(@class, 'ng-star-inserted')]")
    element = WaitForElement(driver, element_locator, 60)
    if element:
        time.sleep(1)
        table_rows = driver.find_elements(
            By.XPATH, "//tr[contains(@class, 'ng-star-inserted')]")

        ScrapingOnlineData(table_rows, input_date, daily_report_id)
    else:
        driver.quit()
    return redirect(reverse('index'))


def WaitForElement(driver, element_locator, wait_time=10):
    try:
        element = WebDriverWait(driver, wait_time).until(
            EC.presence_of_element_located(element_locator))
        return element
    except TimeoutException:
        return None


def ScrapingOnlineData(table_rows, input_date, daily_report_id):

    daily_report = get_object_or_404(DailyReportModel, id=daily_report_id)
    bill_lunch_id = daily_report.bill_lunch.id
    bill_dinner_id = daily_report.bill_dinner.id

    delivery_cash_count = 0
    delivery_card_count = 0
    delivery_cash_amount = 0
    delivery_card_amount = 0
    pickup_cash_count_lunch = 0
    pickup_card_count_lunch = 0
    pickup_cash_amount_lunch = 0
    pickup_card_amount_lunch = 0
    pickup_cash_count_dinner = 0
    pickup_card_count_dinner = 0
    pickup_cash_amount_dinner = 0
    pickup_card_amount_dinner = 0

    for row in table_rows:
        # Get all child <td> elements within the row
        td_elements = row.find_elements(By.TAG_NAME, "td")
        try:
            date = td_elements[1].text
            time = date.split('\n')[0]
            getShiftFromTime = GetShift(time)
            date = date.split('\n')[1]
            shift = getShiftFromTime.lower()
            if date == input_date:
                # Get Shift
                type = td_elements[2].text
                amount = td_elements[4].text
                amount_decimal_format = Decimal(amount[0:6])
                status = td_elements[5].text
                payment_method = td_elements[6].text
                print("type : ", type)
                print("shift : ", shift)
                if status == "Accepted":
                    if type == 'Delivery':
                        if payment_method == "Cash":
                            delivery_cash_count += 1
                            delivery_cash_amount += amount_decimal_format
                        elif payment_method == "Card":
                            delivery_card_count += 1
                            delivery_card_amount += amount_decimal_format
                    elif type == 'Pickup':
                        # Find shift from selected
                        print("amount_decimal_format : ",
                              amount_decimal_format)
                        if shift == 'lunch':
                            if payment_method == "Cash":
                                pickup_cash_count_lunch += 1
                                pickup_cash_amount_lunch += amount_decimal_format
                            elif payment_method == "Card":
                                pickup_card_count_lunch += 1
                                pickup_card_amount_lunch += amount_decimal_format
                        elif shift == 'dinner':
                            if payment_method == "Cash":
                                pickup_cash_count_dinner += 1
                                pickup_cash_amount_dinner += amount_decimal_format
                            elif payment_method == "Card":
                                pickup_card_count_dinner += 1
                                pickup_card_amount_dinner += amount_decimal_format

                print("pickup_cash_count_dinner : ", pickup_cash_count_dinner)
                print("pickup_cash_amount_dinner : ",
                      pickup_cash_amount_dinner)
                print("pickup_card_count_dinner : ", pickup_card_count_dinner)
                print("pickup_card_amount_dinner : ",
                      pickup_card_amount_dinner)

        except:
            pass

        bill_lunch = get_object_or_404(BillLunchModel, id=bill_lunch_id)
        bill_lunch.bill_online_cash_count = pickup_cash_count_lunch
        bill_lunch.bill_online_card_count = pickup_card_count_lunch
        bill_lunch.bill_online_cash = pickup_cash_amount_lunch
        bill_lunch.bill_online_card = pickup_card_amount_lunch
        bill_lunch.save()

        bill_dinner = get_object_or_404(BillDinnerModel, id=bill_dinner_id)
        bill_dinner.bill_online_cash_count = pickup_cash_count_dinner
        bill_dinner.bill_online_card_count = pickup_card_count_dinner
        bill_dinner.bill_online_cash = pickup_cash_amount_dinner
        bill_dinner.bill_online_card = pickup_card_amount_dinner
        bill_dinner.delivery_cash_count_in_online_system = delivery_cash_count
        bill_dinner.delivery_cash_amount_in_online_system = delivery_cash_amount
        bill_dinner.delivery_card_count_in_online_system = delivery_card_count
        bill_dinner.delivery_card_amount_in_online_system = delivery_card_amount
        bill_dinner.save()
    return 0


def GetShift(time_str):
    time_format = "%I:%M %p"
    lunch_start = datetime.datetime.strptime("11:00 AM", time_format).time()
    lunch_end = datetime.datetime.strptime("4:15 PM", time_format).time()
    dinner_start = datetime.datetime.strptime("4:30 PM", time_format).time()
    dinner_end = datetime.datetime.strptime("10:00 PM", time_format).time()

    time_obj = datetime.datetime.strptime(time_str, time_format).time()

    if lunch_start <= time_obj <= lunch_end:
        return "Lunch"
    elif dinner_start <= time_obj <= dinner_end:
        return "Dinner"
    else:
        return "Other Shift"


def ChooseScrapingData(request, daily_report_id):

    context = {}
    daily_report = get_object_or_404(DailyReportModel, id=daily_report_id)
    date = daily_report.date

    context['date'] = date
    context['daily_report_id'] = daily_report_id
    return render(request, 'keywordapp/online-order-scraping.html', context)
# ************************************************************************************************ END : ONLINE ************************************************************************************************


def DeleteDisburse(request, disburse_id, daily_report_id):
    disburse = get_object_or_404(DisburseModel, id=disburse_id)
    disburse.delete()
    return redirect(reverse('disburse-list', kwargs={'daily_report_id': daily_report_id}))

# ************************************************************************************************ START : GENERATE TEXT ************************************************************************************************


def GenerateImageWIthText(sumrealBillOnlineCount, sumrealBillOnline, realBillOnlineCashLunch, realBillOnlineCardLunch, sumrealBillPhoneCount, realBillPhoneLunch, realBillPhoneCashLunch, realBillPhoneCardLunch, sumrealBillInCount, sumrealBillIn, realBillInCashLunch, realBillInCardLunch, realBillHomePhoneCashDinner, realBillHomePhoneCardDinner, sumrealBillHomePhoneCountDinner, sumrealBillHomePhoneDinner, realBillHomeOnlineCashDinner, realBillHomeOnlineCardDinner, sumrealBillHomeOnlineCountDinner, sumrealBillHomeOnlineDinner, sumrealBillPhoneCountDinner, sumrealBillPhoneDinner, realBillPhoneCashDinner, realBillPhoneCardDinner, sumrealBillOnlineCountDinner, sumrealBillOnlineDinner, realBillOnlineCashDinner, realBillOnlineCardDinner, sumrealBillInCountDinner, sumrealBillInDinner, realBillInCashDinner, realBillInCardDinner, sumTotal, sumCash, sumCard, totalBillLunch, totalBillDinner, tipLunch, tipDinner, related_delivery_details, sumrealBillHomeCountDinner, totalSumCommissionAndOa, totalOnlineCount, totalOnlineAmount, day, dateForImage, related_disburse_details, totalSumDisburse, balanceAfterMinusExpense, wrongCreditLunch, wrongCreditDinner):

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
    if sumrealBillOnlineCount != 0:
        imgObj.text((60, 50), str(sumrealBillOnlineCount),
                    font=fontThai, fill=FontColor)  # Total Count
        imgObj.text((90, 50), str("TA Online"), font=fontThai,
                    fill=FontColor)  # Total Count
        imgObj.text((300, 50), str(sumrealBillOnline),
                    font=fontThai, fill=FontColor)  # Total Amount
        imgObj.text((430, 50), str(realBillOnlineCashLunch),
                    font=fontThai, fill=FontColor)  # Cash Amount
        imgObj.text((590, 50), str(realBillOnlineCardLunch),
                    font=fontThai, fill=FontColor)  # Card Amount
    # Row 2 Ta Phone Lunch
    if sumrealBillPhoneCount != 0:
        imgObj.text((60, 130), str(sumrealBillPhoneCount),
                    font=fontThai, fill=FontColor)  # Total Count
        imgObj.text((300, 140), str(realBillPhoneLunch),
                    font=fontThai, fill=FontColor)  # Total Amount
        imgObj.text((430, 140), str(realBillPhoneCashLunch),
                    font=fontThai, fill=FontColor)  # Cash Amount
        imgObj.text((590, 140), str(realBillPhoneCardLunch),
                    font=fontThai, fill=FontColor)  # Card Amount
    else:
        imgObj.text((320, 135), '-', font=fontThai,
                    fill=FontColor)  # Total Amount
        imgObj.text((450, 135), '-', font=fontThai,
                    fill=FontColor)  # Cash Amount
        imgObj.text((610, 135), '-', font=fontThai,
                    fill=FontColor)  # Card Amount
    # Row 3 Dine-in Lunch
    if sumrealBillInCount != 0:
        imgObj.text((60, 170), str(sumrealBillInCount),
                    font=fontThai, fill=FontColor)  # Total Count
        imgObj.text((300, 180), str(sumrealBillIn),
                    font=fontThai, fill=FontColor)  # Total Amount
        imgObj.text((430, 180), str(realBillInCashLunch),
                    font=fontThai, fill=FontColor)  # Cash Amount
        imgObj.text((590, 180), str(realBillInCardLunch),
                    font=fontThai, fill=FontColor)  # Card Amount
    else:
        imgObj.text((320, 175), '-', font=fontThai,
                    fill=FontColor)  # Total Amount
        imgObj.text((450, 175), '-', font=fontThai,
                    fill=FontColor)  # Cash Amount
        imgObj.text((610, 175), '-', font=fontThai,
                    fill=FontColor)  # Card Amount
    # Row 4 Home Phone
    if sumrealBillHomePhoneCountDinner != 0:
        imgObj.text((60, 210), str(sumrealBillHomePhoneCountDinner),
                    font=fontThai, fill=FontColor)  # Total Count
        imgObj.text((300, 220), str(sumrealBillHomePhoneDinner),
                    font=fontThai, fill=FontColor)  # Total Amount
        imgObj.text((430, 220), str(realBillHomePhoneCashDinner),
                    font=fontThai, fill=FontColor)  # Cash Amount
        imgObj.text((590, 220), str(realBillHomePhoneCardDinner),
                    font=fontThai, fill=FontColor)  # Card Amount
    else:
        imgObj.text((320, 215), '-', font=fontThai,
                    fill=FontColor)  # Total Amount
        imgObj.text((450, 215), '-', font=fontThai,
                    fill=FontColor)  # Cash Amount
        imgObj.text((610, 215), '-', font=fontThai,
                    fill=FontColor)  # Card Amount
    # Row 5 Home Online
    if sumrealBillHomeOnlineCountDinner != 0:
        imgObj.text((60, 250), str(sumrealBillHomeOnlineCountDinner),
                    font=fontThai, fill=FontColor)  # Total Count
        imgObj.text((300, 260), str(sumrealBillHomeOnlineDinner),
                    font=fontThai, fill=FontColor)  # Total Amount
        imgObj.text((430, 260), str(realBillHomeOnlineCashDinner),
                    font=fontThai, fill=FontColor)  # Cash Amount
        imgObj.text((590, 260), str(realBillHomeOnlineCardDinner),
                    font=fontThai, fill=FontColor)  # Card Amount
    else:
        imgObj.text((320, 255), '-', font=fontThai,
                    fill=FontColor)  # Total Amount
        imgObj.text((450, 255), '-', font=fontThai,
                    fill=FontColor)  # Cash Amount
        imgObj.text((610, 255), '-', font=fontThai,
                    fill=FontColor)  # Card Amount
    # Row 6 T/A Phone Dinner
    if sumrealBillPhoneCountDinner != 0:
        imgObj.text((60, 290), str(sumrealBillPhoneCountDinner),
                    font=fontThai, fill=FontColor)  # Total Count
        imgObj.text((300, 300), str(sumrealBillPhoneDinner),
                    font=fontThai, fill=FontColor)  # Total Amount
        imgObj.text((430, 300), str(realBillPhoneCashDinner),
                    font=fontThai, fill=FontColor)  # Cash Amount
        imgObj.text((590, 300), str(realBillPhoneCardDinner),
                    font=fontThai, fill=FontColor)  # Card Amount
    else:
        imgObj.text((320, 295), '-', font=fontThai,
                    fill=FontColor)  # Total Amount
        imgObj.text((450, 295), '-', font=fontThai,
                    fill=FontColor)  # Cash Amount
        imgObj.text((610, 295), '-', font=fontThai,
                    fill=FontColor)  # Card Amount
    # Row 7 T/A Online Dinner
    if sumrealBillOnlineCountDinner != 0:
        imgObj.text((60, 330), str(sumrealBillOnlineCountDinner),
                    font=fontThai, fill=FontColor)  # Total Count
        imgObj.text((300, 340), str(sumrealBillOnlineDinner),
                    font=fontThai, fill=FontColor)  # Total Amount
        imgObj.text((430, 340), str(realBillOnlineCashDinner),
                    font=fontThai, fill=FontColor)  # Cash Amount
        imgObj.text((590, 340), str(realBillOnlineCardDinner),
                    font=fontThai, fill=FontColor)  # Card Amount
    else:
        imgObj.text((320, 335), '-', font=fontThai,
                    fill=FontColor)  # Total Amount
        imgObj.text((450, 335), '-', font=fontThai,
                    fill=FontColor)  # Cash Amount
        imgObj.text((610, 335), '-', font=fontThai,
                    fill=FontColor)  # Card Amount
    # Row 8 Dine-in Dinner
    if sumrealBillInCountDinner != 0:
        imgObj.text((60, 380), str(sumrealBillInCountDinner),
                    font=fontThai, fill=FontColor)  # Total Count
        imgObj.text((300, 380), str(sumrealBillInDinner),
                    font=fontThai, fill=FontColor)  # Total Amount
        imgObj.text((430, 380), str(realBillInCashDinner),
                    font=fontThai, fill=FontColor)  # Cash Amount
        imgObj.text((590, 380), str(realBillInCardDinner),
                    font=fontThai, fill=FontColor)  # Card Amount
    else:
        imgObj.text((320, 375), '-', font=fontThai,
                    fill=FontColor)  # Total Amount
        imgObj.text((450, 375), '-', font=fontThai,
                    fill=FontColor)  # Cash Amount
        imgObj.text((610, 375), '-', font=fontThai,
                    fill=FontColor)  # Card Amount
    # Row 9 Total

    if sumTotal != 0:
        imgObj.text((300, 420), str(sumTotal), font=fontThai,
                    fill=FontColor)  # Total Amount
        AddTransparentHighlight(img, str(sumTotal), (300, 420),
                                fontTotalShift, 0.2, 'orange')
        imgObj.text((430, 420), str(sumCash), font=fontThai,
                    fill=FontColor)  # Cash Amount
        AddTransparentHighlight(img, str(sumCash), (430, 420),
                                fontTotalShift, 0.2, 'orange')
        imgObj.text((590, 420), str(sumCard), font=fontThai,
                    fill=FontColor)  # Card Amount
        AddTransparentHighlight(img, str(sumCard), (590, 420),
                                fontTotalShift, 0.2, 'orange')
    else:
        imgObj.text((320, 410), '-', font=fontTotalShift,
                    fill=FontColor)  # Total Amount
        imgObj.text((450, 410), '-', font=fontTotalShift,
                    fill=FontColor)  # Total Amount
        imgObj.text((610, 410), '-', font=fontTotalShift,
                    fill=FontColor)  # Total Amount
    # Right Column
    if totalBillLunch != 0:
        imgObj.text((760, 160), str(totalBillLunch),
                    font=fontTotalShift, fill=FontColor)  # Total Bill Lunch
        AddTransparentHighlight(img, str(totalBillLunch),
                                (760, 160), fontTotalShift, 0.2, 'orange')
    else:
        imgObj.text((760, 160), '-', font=fontTotalShift,
                    fill=FontColor)  # Total Amount

    if totalBillDinner != 0:
        imgObj.text((710, 300), str(totalBillDinner),
                    font=fontTotalShift, fill=FontColor)  # Total Bill Dinner
        AddTransparentHighlight(img, str(totalBillDinner),
                                (710, 300), fontTotalShift, 0.2, 'orange')
    else:
        imgObj.text((780, 300), '-', font=fontTotalShift,
                    fill=FontColor)  # Total Amount
    # Tip

    if tipLunch != 0:
        imgObj.text((590, 470), str('Tip Lunch '+str(tipLunch)),
                    font=fontThai, fill=FontColor)  # Tip Lunch
        AddTransparentHighlight(img, str('Tip Lunch '),
                                (590, 470), fontTotalShift, 0.5, 'pink')
    if tipDinner != 0:
        imgObj.text((590, 500), str('Tip Dinner '+str(tipDinner)),
                    font=fontThai, fill=FontColor)  # Tip Dinner
        AddTransparentHighlight(img, str('Tip Dinner '),
                                (590, 500), fontTotalShift, 0.5, 'pink')

    # Home Delivery
    homePosXHomeCount = 100
    homePosYHomeCount = 545
    homePosXShowOaCount = 120
    homePosYShowOaCount = 545
    homePosXSumCommission = 330
    homePosYSumCommission = 545
    homePosXShowOaAmount = 360
    homePosYShowOaAmount = 545
    homePosXDeliveryName = 420
    homePosYDeliveryName = 545
    if related_delivery_details != 0:
        for item in related_delivery_details:
            imgObj.text((homePosXHomeCount, homePosYHomeCount), str(
                item.home_count), font=fontThai, fill=FontColor)  # Home Count
            imgObj.text((homePosXShowOaCount, homePosYShowOaCount), str(
                item.show_oa_count), font=fontThai, fill=FontColor)  # Show OA Count
            imgObj.text((homePosXSumCommission, homePosYSumCommission), str(
                item.sum_commission), font=fontThai, fill=FontColor)  # Sum Commission
            imgObj.text((homePosXShowOaAmount, homePosYShowOaAmount), str(
                item.show_oa_amount), font=fontThai, fill=FontColor)  # Show OA Amount
            imgObj.text((homePosXDeliveryName, homePosYDeliveryName), str(
                item.delivery_name), font=fontThai, fill=FontColor)  # Show Delivery name
            # Step position down
            homePosYHomeCount += 45
            homePosYShowOaCount += 45
            homePosYSumCommission += 45
            homePosYShowOaAmount += 45
            homePosYDeliveryName += 45
    print("totalSumCommissionAndOa :", totalSumCommissionAndOa)
    if sumrealBillHomeCountDinner != 0:
        imgObj.text((100, 670), str(sumrealBillHomeCountDinner)+'                      ' +
                    str(totalSumCommissionAndOa), font=fontThai, fill=FontColor)  # Total Delivery
        AddTransparentHighlight(img, str(sumrealBillHomeCountDinner) +
                                '                   ', (100, 670), fontTotalShift, 0.2, 'pink')

    # Total Online
    if totalOnlineCount != 0:
        imgObj.text((690, 545), '('+str(totalOnlineCount)+') ' +
                    str(totalOnlineAmount), font=fontThai, fill=FontColor)  # Total Online
        AddTransparentHighlight(img, '  '+str(totalOnlineAmount),
                                (690, 545), fontTotalShift, 0.2, 'orange')

    # Wrong Credit
    if wrongCreditLunch != 0:
        imgObj.text((550, 700), 'กดเครดิตขาด(เที่ยง) '+str(wrongCreditLunch),
                    font=fontThai, fill=FontColor)  # Wrong Credit Lunch
        AddTransparentHighlight(
            img, '                     ', (550, 700), fontTotalShift, 0.2, 'orange')

    if wrongCreditDinner != 0:
        imgObj.text((550, 730), 'กดเครดิตขาด(เย็น) '+str(wrongCreditDinner),
                    font=fontThai, fill=FontColor)  # Wrong Credit Dinner
        AddTransparentHighlight(
            img, '                     ', (550, 730), fontTotalShift, 0.2, 'orange')

    # Dairy Record
    imgObj.text((1000, 90), str(day), font=fontThai, fill=FontColor)  # Day
    imgObj.text((1000, 130), str(dateForImage),
                font=fontThai, fill=FontColor)  # Date

    # Dairy Expense
    if related_disburse_details != 0:
        ExpensePosX = 950
        ExpensePosY = 380
        for item in related_disburse_details:
            imgObj.text((ExpensePosX, ExpensePosY), str(
                str(item.name)+'  '+str(item.price)), font=fontThai, fill=FontColor)  # Expense
            # Step position down
            ExpensePosY += 40

    if totalSumDisburse != 0:
        imgObj.text((980, 780), str(totalSumDisburse),
                    font=fontTotalShift, fill=FontColor)  # Total
        AddTransparentHighlight(
            img, str(totalSumDisburse), (980, 780), fontTotalShift, 0.5, 'pink')

    # Balance
    if balanceAfterMinusExpense != 0:
        imgObj.text((350, 780), str(balanceAfterMinusExpense),
                    font=fontTotalShift, fill=FontColor)  # Balance
        AddTransparentHighlight(
            img, str(balanceAfterMinusExpense), (350, 780), fontTotalShift, 0.2, 'orange')

    locationSaved = path+'/static/img/result.jpg'
    img.save(locationSaved)
    imgLocation = '/static/img/result.jpg'

    return imgLocation


def AddTransparentHighlight(image, text, text_position, font, opacity, color='orange'):
    # Create a new transparent image with the same size as the original image
    rect_img = Image.new('RGBA', image.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(rect_img)

    # Draw the text on the transparent image
    draw.text(text_position, text, font=font)

    # Calculate the size of the text
    text_width, text_height = draw.textsize(text, font=font)

    # Define the coordinates of the rectangle that will surround the text
    rect_x1, rect_y1 = text_position
    rect_x2, rect_y2 = text_position[0] + \
        text_width, text_position[1] + text_height

    # Calculate the fill color with the specified opacity
    if color == 'orange':
        fill_color = (255, 69, 0, int(255 * opacity))
    elif color == 'pink':
        fill_color = (255, 105, 180, int(255 * opacity))

    # Draw a filled and transparent rectangle around the text
    draw.rectangle([rect_x1, rect_y1, rect_x2, rect_y2],
                   outline=None, fill=fill_color)

    # Paste the transparent rectangle image over the original image
    image.paste(rect_img, (0, 0), rect_img)
# ************************************************************************************************ END : GENERATE TEXT ************************************************************************************************

# ************************************************************************************************ START : EMAIL ************************************************************************************************


def UpdatePosData(request, daily_report_id,):

    daily_object = get_object_or_404(DailyReportModel, id=daily_report_id)
    selectedDate = daily_object.date
    # Your Outlook email credentials
    username = 'cheetah6541@gmail.com'
    password = 'bitjqffhoygdllid'

    # Outlook IMAP server and port
    imap_ssl_host = 'imap.gmail.com'  # imap.mail.yahoo.com
    imap_ssl_port = 993
    try:
        mail = imaplib.IMAP4_SSL(imap_ssl_host, imap_ssl_port)
        # Log in to your email account
        mail.login(username, password)

        # Select the mailbox (folder) you want to read emails from (e.g., INBOX)
        mailbox = 'INBOX'
        mail.select(mailbox)
    except:
        print("ERROR")

# Search for emails (optional)
# Here, we search for all emails in the selected mailbox
    sender_email = 'judy888123@gmail.com'
    # sender_email = 'cheetah5900@windowslive.com'
    # subject = 'Z Reading Report'
    print("selectedDate : ", selectedDate)
    search_query = f'(FROM "{sender_email}" SUBJECT "{selectedDate}")'
    status, email_ids = mail.search(None, search_query)

    # * Delete old file
    path = os.getcwd()
    if settings.PC_OR_MAC == "PC":
        save_path = path + r'\static\mail'
    elif settings.PC_OR_MAC == "MAC":
        save_path = path + '/static/mail'
    files = os.listdir(save_path)
    # Iterate through the files and delete them
    for file in files:
        file_path_for_delete = os.path.join(save_path, file)
        try:
            if os.path.isfile(file_path_for_delete):
                os.remove(file_path_for_delete)
                print(f"Deleted: {file_path_for_delete}")
            else:
                print(f"Skipped (not a file): {file_path_for_delete}")
        except Exception as e:
            print(f"Error deleting {file_path_for_delete}: {e}")

    # Loop through all email IDs
    for email_id in email_ids[0].split():
        # Fetch the email content
        status, email_data = mail.fetch(email_id, '(RFC822)')
        raw_email = email_data[0][1]
        # Parse the email content
        msg = email.message_from_bytes(raw_email)

        # Check if the email has any attachments
        if msg.get_content_maintype() == 'multipart':
            for part in msg.walk():
                if part.get_content_maintype() == 'multipart' or part.get('Content-Disposition') is None:
                    continue
                filename = part.get_filename()
                if filename:
                    new_filename_html = f"{selectedDate}.html"
                    # Save the attachment to a specific folder
                    path = os.getcwd()
                    if settings.PC_OR_MAC == "PC":
                        save_path = path + r'\static\mail'
                    elif settings.PC_OR_MAC == "MAC":
                        save_path = path + '/static/mail'
                    if not os.path.exists(save_path):
                        os.makedirs(save_path)

                    file_path = os.path.join(save_path, new_filename_html)
                    file_path = get_unique_file_name(file_path)
                    with open(file_path, 'wb') as f:
                        f.write(part.get_payload(decode=True))
                    print(f'Saved attachment: {new_filename_html}')

    mail.logout()
    # Loop to do every file in folder
    path = os.getcwd()
    if settings.PC_OR_MAC == "PC":
        save_path = path + r'\static\mail'
    elif settings.PC_OR_MAC == "MAC":
        save_path = path + '/static/mail'

    files_in_folder = os.listdir(save_path)
    files_with_selected_date = [
        file for file in files_in_folder if str(selectedDate) in file]
    file_count = len(files_with_selected_date)

    for i in range(file_count):
        file_name = files_with_selected_date[i]
        file_path = os.path.join(save_path, file_name)
        try:
            tables = pd.read_html(file_path)
        except:
            return redirect('index')
        if tables:
            table_df = tables[0]

            # Check if the DataFrame is not empty and has rows and columns
            if not table_df.empty:
                # Get the number of rows and columns in the DataFrame
                num_rows, num_cols = table_df.shape

                # Iterate through the rows and columns to extract cell values
                for row in range(num_rows):
                    for col in range(num_cols):
                        # Access cell value by index
                        cell_value = table_df.iat[row, col]
                        print(f"Cell ({row}, {col}):", cell_value)
            else:
                print("Table DataFrame is empty.")
        else:
            print("No tables found on the page.")
        #! ================================================================= START : GET COUNT AND AMOUNT =================================================================
        # ? Identify POS type
        # Get cell values from tax information table
        # If it can find the text this will be normal ta report
        # todo ================= NORMAL TA REPORT ========================
        getGstSales1 = table_df.iat[21, 0]
        findGstSales1 = getGstSales1.find("GST Sales")
        try:
            # todo ================= ABNORMAL TA REPORT ========================
            getGstSales2 = table_df.iat[25, 0]
            findGstSales2 = getGstSales2.find("GST Sales")
        except:
            findGstSales2 = -1
        if findGstSales1 != -1:
            posType = "ta"
            # ? Identify Format type
            getToGoValue = table_df.iat[2, 0]
            findTheWordToGo = getToGoValue.lower().find("to go")
            # If found To Go index. it means there is the word "To Go" there.
            # TA normal
            if findTheWordToGo != -1:
                countAll = GetNumberAfterDashSign(getToGoValue)
                cashCount, cashAmount, cardCount, cardAmount = getCashAndCardData(
                    table_df, 24)
            else:
                print("Can't find word To Go")
            # If can't find To Go at that row. it means it is abnormal bill
        elif findGstSales2 != -1:
            # TA abnormal
            posType = "ta"
            # ? Identify Format type
            getToGoValue = table_df.iat[4, 0]
            getDeliveryValue = table_df.iat[5, 0]
            findTheWordToGo = getToGoValue.lower().find("to go")
            if findTheWordToGo != -1:
                countAllToGo = GetNumberAfterDashSign(getToGoValue)
                countAllDelivery = GetNumberAfterDashSign(getDeliveryValue)
                countAll = int(countAllToGo) + int(countAllDelivery)
                cashCount, cashAmount, cardCount, cardAmount = getCashAndCardData(
                    table_df, 28)
            else:
                print("Can't find word To Go")
        else:
            posType = "in"
            # ? Reformat dine in format
            indent_html_file(file_path, file_path)
            # ? read file again
            tables = pd.read_html(file_path)
            if tables:
                table_df = tables[0]
            # ? Identify Format type
            getDineInValue = table_df.iat[0, 1]
            findTheWordDineIn = getDineInValue.lower().find("dine in")
            # Dine in normal
            if findTheWordDineIn != -1:
                # Check last row of  Sales Report table 2 position
                getSalesTaxRounding1 = table_df.iat[22, 0]
                getSalesTaxRounding2 = table_df.iat[23, 0]
                getSalesTaxRounding3 = table_df.iat[26, 0]
                getSalesTaxRounding4 = table_df.iat[27, 0]
                # If it can find the text this will be normal dine in report
                # todo ================= NORMAL DINE IN REPORT ========================
                findTheWordSalesTaxRounding1 = getSalesTaxRounding1.lower().find(
                    "sales + tax + rounding")
                # If it can find the text this will be normal dine in report but there is Unpaid order.
                # todo ================= NORMAL DINE IN REPORT WITH UNPAID ORDER ========================
                findTheWordSalesTaxRounding2 = getSalesTaxRounding2.lower().find(
                    "sales + tax + rounding")
                # todo ================= ABNORMAL DINE IN REPORT ========================
                findTheWordSalesTaxRounding3 = getSalesTaxRounding3.lower().find(
                    "sales + tax + rounding")
                # todo ================= ABNORMAL DINE IN REPORT WITH UNPAID ORDER ========================
                findTheWordSalesTaxRounding4 = getSalesTaxRounding4.lower().find(
                    "sales + tax + rounding")

                if findTheWordSalesTaxRounding1 != -1:
                    getCountAll = table_df.iat[3, 0]
                    countAll = GetNumberAfterDashSign(getCountAll)
                    rowForCheckingMoney = 24
                elif findTheWordSalesTaxRounding2 != -1:
                    getCountAll = table_df.iat[4, 0]
                    countAll = GetNumberAfterDashSign(getCountAll)
                    rowForCheckingMoney = 25
                elif findTheWordSalesTaxRounding3 != -1:
                    countDineIn = table_df.iat[4, 0]
                    countToGo = table_df.iat[5, 0]
                    countAll = int(countDineIn) + int(countToGo)
                    rowForCheckingMoney = 28
                elif findTheWordSalesTaxRounding4 != -1:
                    countDineIn = table_df.iat[5, 0]
                    countToGo = table_df.iat[6, 0]
                    countAll = int(countDineIn) + int(countToGo)
                    rowForCheckingMoney = 29
                else:
                    print("Can't find sales + tax + rounding")

                cashCount, cashAmount, cardCount, cardAmount = getCashAndCardData(
                    table_df, rowForCheckingMoney)
            else:
                print("Can't find word dine in")
        #! ================================================================= END : GET COUNT AND AMOUNT =================================================================

        #! ================================================================= START : GET SHIFT =================================================================
        # ? Identify shift
        getShiftName = table_df.iat[0, 1]
        shiftNameIndex = getShiftName.find("Shift Name:")
        if shiftNameIndex != -1:
            # Get the word after "Shift Name:"
            shiftName = getShiftName[shiftNameIndex +
                                     11:shiftNameIndex + 11 + 6].strip().lower()
            if 'din' in shiftName:
                shift = "dinner"
            elif shiftName == "lunch":
                shift = "lunch"
            else:
                print("Can't Identify shift")
        else:
            print("No 'Shift Name:' found in the table.")

        #! ================================================================= START : ADD DATA TO DB =================================================================
        if posType == "ta":
            if shift == "lunch":
                bill_lunch_id = daily_object.bill_lunch.id
                bill_lunch = BillLunchModel.objects.get(id=bill_lunch_id)
                # POS TA Phone
                bill_lunch.pos_ta_bill_phone_cash = cashAmount
                bill_lunch.pos_ta_bill_phone_cash_count = cashCount
                bill_lunch.pos_ta_bill_phone_card = cardAmount
                bill_lunch.pos_ta_bill_phone_card_count = cardCount
                bill_lunch.pos_ta_phone_total_bill_count = countAll
                # Save the updated object
                bill_lunch.save()
            elif shift == "dinner":
                bill_dinner_id = daily_object.bill_dinner.id
                bill_dinner = BillDinnerModel.objects.get(id=bill_dinner_id)
                # POS Dine in
                bill_dinner.pos_ta_bill_phone_cash = cashAmount
                bill_dinner.pos_ta_bill_phone_cash_count = cashCount
                bill_dinner.pos_ta_bill_phone_card = cardAmount
                bill_dinner.pos_ta_bill_phone_card_count = cardCount
                bill_dinner.pos_ta_phone_total_bill_count = countAll
                bill_dinner.save()
        if posType == "in":
            if shift == "lunch":
                bill_lunch_id = daily_object.bill_lunch.id
                bill_lunch = BillLunchModel.objects.get(id=bill_lunch_id)
                # POS TA Phone
                bill_lunch.pos_in_bill_cash = cashAmount
                bill_lunch.pos_in_bill_cash_count = cashCount
                bill_lunch.pos_in_bill_card = cardAmount
                bill_lunch.pos_in_bill_card_count = cardCount
                bill_lunch.pos_dine_in_total_bill_count = countAll
                # Save the updated object
                bill_lunch.save()
            elif shift == "dinner":
                bill_dinner_id = daily_object.bill_dinner.id
                bill_dinner = BillDinnerModel.objects.get(id=bill_dinner_id)
                # POS Dine in
                bill_dinner.pos_in_bill_cash = cashAmount
                bill_dinner.pos_in_bill_cash_count = cashCount
                bill_dinner.pos_in_bill_card = cardAmount
                bill_dinner.pos_in_bill_card_count = cardCount
                bill_dinner.pos_dine_in_total_bill_count = countAll
                bill_dinner.save()

    return render(request, 'keywordapp/after-pos-scraping.html', context={'daily_report_id': daily_report_id})

# ************************************************************************************************ END : EMAIL ************************************************************************************************


def GetNumberAfterDashSign(cellData):
    splitCellData = cellData.split("-")
    result = int(splitCellData[1].strip())

    return result


def getCashAndCardData(table_df, rowCash):
    cashCount = 0
    cashAmount = 0
    cardCount = 0
    cardAmount = 0
    # Cash Topic Cell
    getCashCount = table_df.iat[rowCash, 0]
    print("getCashCount : ", getCashCount)
    if getCashCount != "Cash":
        cashCount = GetNumberAfterDashSign(getCashCount)
        print("cashCount : ", cashCount)
        cashAmount = table_df.iat[rowCash, 1]
        print("cashAmount : ", cashAmount)
    # Card Topic Cell
    getCardCount = table_df.iat[rowCash+1, 0]
    print("getCardCount : ", getCardCount)
    if getCardCount != "Credit card":
        cardCount = GetNumberAfterDashSign(getCardCount)
        print("cardCount : ", cardCount)
        cardAmount = table_df.iat[rowCash+1, 1]
        print("cardAmount : ", cardAmount)
    return cashCount, cashAmount, cardCount, cardAmount


def indent_html_file(input_file_path, output_file_path):
    with open(input_file_path, 'r', encoding='utf-8') as file:
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(file, 'html.parser')

    # Use prettify() method to add indentation
    indented_html = soup.prettify()

    # Write the indented HTML to the output file
    with open(output_file_path, 'w', encoding='utf-8') as outfile:
        outfile.write(indented_html)


# Define a function to handle duplicated file names
def get_unique_file_name(file_path):
    count = 1
    base_name, ext = os.path.splitext(file_path)
    while os.path.exists(file_path):
        file_path = f"{base_name}_{count}{ext}"
        count += 1
    return file_path
