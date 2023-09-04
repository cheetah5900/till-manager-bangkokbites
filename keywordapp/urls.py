from django.urls import path
from keywordapp.views import *

urlpatterns = [
    path('', Index, name='index'),
    path('<str:branch>/<int:daily_report_id>', ChooseMode, name='choose-mode'),

    # ? Disburse
    path('disburse-input/<str:daily_report_id>/<int:disburse_id>/',
         DisburseInput, name='disburse-input'),
    path('delete-disburse/<int:disburse_id>/<str:daily_report_id>/',
         DeleteDisburse, name='delete-disburse'),

    # ? Lunch
    path('lunch-report/<str:daily_report_id>/',
         LunchReport, name='lunch-report'),

    # ? Dinner
    path('dinner-report/<str:branch>/<int:daily_report_id>/',
         DinnerReport, name='dinner-report'),

    # ? Home
    path('home-report/<str:daily_report_id>/<int:delivery_id>/',
         HomeInputDetail, name='home-report'),
    path('delete-delivery-detail/<int:delivery_detail_id>/<str:daily_report_id>/',
         DeleteDeliveryDetail, name='delete-delivery-detail'),


    # ? Scraping Data
    path('scraping/<str:daily_report_id>/',
         ChooseScrapingData, name='scraping'),
    path('get-online-data/<str:daily_report_id>/', GetOnlineOrderData),

    # ? POS update
    path('update-pos/<str:daily_report_id>/', UpdatePosData,name='update-pos'),
]
