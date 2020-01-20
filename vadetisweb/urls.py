from django.urls import path
from vadetisweb import views

app_name = 'vadetisweb'

urlpatterns = [

    path('accounts/application-settings/', views.ApplicationSettings.as_view(), name='application_settings'),
    path('account/datasets', views.account_datasets, name='account_datasets'),
    path('account/training-datasets', views.account_training_datasets, name='account_training_datasets'),
    path('account', views.account, name='account'),

    path('', views.index, name='index'),

]
