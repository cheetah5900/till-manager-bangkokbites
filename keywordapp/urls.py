from django.urls import path
from keywordapp.views import *

urlpatterns = [
    path('', Index, name='index'),

    # ? Disburse
    path('disburse-list/<str:daily_report_id>/',
         DisburseList, name='disburse-list'),
    path('disburse-input/<str:daily_report_id>/<int:disburse_id>/',
         DisburseInput, name='disburse-input'),
    path('delete-disburse/<int:disburse_id>/<str:daily_report_id>/',
         DeleteDisburse, name='delete-disburse'),

    # ? Lunch
    path('lunch-input-quick/<str:daily_report_id>/',
         LunchInputQuick, name='lunch-input-quick'),
    path('lunch-input-detail/<str:daily_report_id>/',
         LunchInputDetail, name='lunch-input-detail'),
    path('lunch-report/<str:daily_report_id>/',
         LunchReport, name='lunch-report'),

    # ? Dinner
    path('dinner-input-quick/<str:daily_report_id>/',
         DinnerInputQuick, name='dinner-input-quick'),
    path('dinner-input-detail/<str:daily_report_id>/',
         DinnerInputDetail, name='dinner-input-detail'),
    path('dinner-report/<str:daily_report_id>/',
         DinnerReport, name='dinner-report'),

    # ? Home
    path('home-list/<str:daily_report_id>/', HomeList, name='home-list'),
    path('home-input-quick/<str:daily_report_id>/<int:delivery_id>/',
         HomeInputQuick, name='home-input-quick'),
    path('home-input-detail/<str:daily_report_id>/<int:delivery_id>/',
         HomeInputDetail, name='home-input-detail'),
    path('delete-delivery-detail/<int:delivery_detail_id>/<str:daily_report_id>/',
         DeleteDeliveryDetail, name='delete-delivery-detail'),


    # ? Scraping Data
    path('scraping/<str:daily_report_id>/',
         ChooseScrapingData, name='scraping'),
    path('get-online-data/<str:daily_report_id>/', GetOnlineOrderData),

    # ? POS update
    path('update-pos/<str:daily_report_id>/', UpdatePosData),
]
