from django.conf.urls import url
from . import views

urlpatterns=[
    url('^$',views.welcome,name = 'welcome'),
    url('access/token', views.getAccessToken, name='get_mpesa_access_token'),
    url('online/lipa', views.lipa_na_mpesa_online, name='lipa_na_mpesa'),

# register, confirmation, validation and callback urls
    url('c2b/register', views.register_urls, name="register_mpesa_validation"),
    url('c2b/confirmation', views.confirmation, name="confirmation"),
    url('c2b/validation', views.validation, name="validation"),
    url('c2b/callback', views.call_back, name="call_backurl"),

# payment, combinedbills

    url('^combinedReport/', views.combinedReport, name='combinedReport'),
    url('^payment', views.payment, name='payment'),

# API 

    url('^api/bills/', views.BillsList.as_view()),
    url('^all_customer_bills/', views.all_customer_bills, name='all_customer_bills'),


]