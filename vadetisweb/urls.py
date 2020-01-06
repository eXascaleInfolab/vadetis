from django.urls import path
from vadetisweb import views

app_name = 'vadetisweb'

urlpatterns = [

    path('account', views.account, name='account'),

    path('', views.index, name='index'),

]
