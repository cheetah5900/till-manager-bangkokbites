from django.urls import path
from keywordapp.views import *

urlpatterns = [
    path('', Index, name='index'),
    path('<str:branch>/<int:daily_report_id>', ChooseMode, name='choose-mode'),

    # ? Disburse
    path('disburse/<str:branch>/<str:daily_report_id>/',
         DisburseInput,),
    path('disburse-edit/<str:branch>/<str:daily_report_id>/<int:disburse_id>/',
         DisburseEdit, name='disburse-input'),
    path('delete-disburse/<str:branch>/<int:disburse_id>/<str:daily_report_id>/',
         DeleteDisburse, name='delete-disburse'),

    # ? Lunch
    path('lunch/<str:branch>/<str:daily_report_id>/',
         LunchInput,),
    path('lunch-report/<str:daily_report_id>/',
         LunchReport, name='lunch-report'),

    # ? Dinner
    path('dinner/<str:branch>/<str:daily_report_id>/',
         DinnerInput,),
    path('dinner-report/<str:branch>/<int:daily_report_id>/',
         DinnerReport, name='dinner-report'),

    # ? Home
    path('home/<str:branch>/<str:daily_report_id>/',
         HomeInput,),
    path('home-edit/<str:branch>/<str:daily_report_id>/<int:delivery_id>/',
         HomeEdit, name='home-edit'),
    path('delete-delivery-detail/<str:branch>/<str:daily_report_id>/<int:delivery_detail_id>/',
         DeleteDeliveryDetail, name='delete-delivery-detail'),
    path('home-report/<str:branch>/<str:daily_report_id>/<int:delivery_id>/',
         HomeReport, name='home-report'),


    # ? Scraping Data
    path('scraping/<str:daily_report_id>/',
         ChooseScrapingData, name='scraping'),
    path('get-online-data/<str:daily_report_id>/', GetOnlineOrderData),

    # ? POS update
    path('update-pos/<str:daily_report_id>/',
         UpdatePosData, name='update-pos'),
]
