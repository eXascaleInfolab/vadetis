from django.urls import path
from vadetisweb import views

app_name = 'vadetisweb'

urlpatterns = [

    path('api/account/datasets', views.AccountDatasets.as_view(), name='account_datasets'),
    path('api/account/training-datasets', views.AccountTrainingDatasets.as_view(), name='account_training_datasets'),

    path('accounts/application-settings/', views.ApplicationSettings.as_view(), name='application_settings'),
    path('account/datasets', views.account_datasets, name='account_datasets'),
    path('account/datasets/upload', views.AccountUploadDataset.as_view(), name='account_datasets_upload'),
    path('account/training-datasets', views.account_training_datasets, name='account_training_datasets'),
    path('account/training-datasets/upload', views.AccountUploadTrainingDataset.as_view(), name='account_training_datasets_upload'),
    path('account', views.account, name='account'),

    path('', views.index, name='index'),

]
