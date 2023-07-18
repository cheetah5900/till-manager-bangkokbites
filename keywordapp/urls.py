from django.urls import path
from keywordapp.views import *

urlpatterns = [
    path('', Index, name='index'),
    path('home-input/', HomeInput),
    path('lunch-input-detail/<str:daily_report_id>/', LunchInputDetail, name='lunch-input'),
    path('lunch-input-quick/<str:daily_report_id>/', LunchInputQuick, name='lunch-input-quick'),
    path('lunch-result/<str:daily_report_id>/', LunchResult,name='lunch-result'),
    path('lunch-report/<str:daily_report_id>/', LunchReport,name='lunch-report'),
    path('dinner-input/', DinnerInput),
    path('home-result/', HomeResult),
]
