from django.conf.urls import url
from . import views

urlpatterns=[
    url('^$',views.welcome,name = 'welcome'),
    url('access/token', views.getAccessToken, name='get_mpesa_access_token'),

]