from django.urls import path
from keywordapp.views import *

urlpatterns = [
    path('', Index, name='index'),
    path('home-input/', HomeInput),
    path('lunch-input-quick/<str:daily_report_id>/', LunchInputQuick, name='lunch-input-quick'),
    path('lunch-input-detail/<str:daily_report_id>/', LunchInputDetail, name='lunch-input-detail'),
    path('lunch-result/<str:daily_report_id>/', LunchResult,name='lunch-result'),
    path('lunch-report/<str:daily_report_id>/', LunchReport,name='lunch-report'),
    
    #? Dinner
    path('dinner-input-quick/<str:daily_report_id>/', DinnerInputQuick, name='dinner-input-quick'),
    path('dinner-input-detail/<str:daily_report_id>/', DinnerInputDetail, name='dinner-input-detail'),
    path('dinner-result/<str:daily_report_id>/', DinnerResult,name='dinner-result'),
    path('dinner-report/<str:daily_report_id>/', DinnerReport,name='dinner-report'),
    
    path('dinner-input/', DinnerInput),
    path('home-result/', HomeResult),
]
