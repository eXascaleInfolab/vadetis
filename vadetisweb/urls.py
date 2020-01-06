from django.urls import path
from vadetisweb import views

app_name = 'vadetisweb'

urlpatterns = [

    path('accounts/application-settings/', views.application_settings, name='application_settings'),
    path('account', views.account, name='account'),

    path('', views.index, name='index'),

]
