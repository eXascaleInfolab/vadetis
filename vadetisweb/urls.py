from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework import routers

from vadetisweb import views

app_name = 'vadetisweb'

"""
    format patterns: provide either rendered view or json, depending if ajax is used, 
    we do not use format_suffix_patterns as we use query parameter (e.g. ?format=json)
    
    api paths: provide data as json
"""

router = routers.DefaultRouter()
router.register(r'account/datasets', views.DatasetDataTableViewSet, base_name='account_datasets_datatable')
router.register(r'account/training-datasets', views.TrainingDatasetDataTableViewSet, base_name='account_training_datasets_datatable')

urlpatterns = [

    path('account/datasets/upload/', views.AccountUploadDataset.as_view(), name='account_datasets_upload'),
    path('account/training-datasets/upload/', views.AccountUploadTrainingDataset.as_view(), name='account_training_datasets_upload'),

    path('api/', include((router.urls))),
    path('api/datasets/real-world/', views.RealWorldDatasetsJson.as_view(), name='real_world_datasets_json'),
    path('api/datasets/synthetic/', views.SyntheticDatasetsJson.as_view(), name='synthetic_datasets_json'),
    path('api/dataset/<int:dataset_id>/', views.DatasetJson.as_view(), name='dataset_json'),

    path('datasets/real-world/', views.RealWorldDatasets.as_view(), name='real_world_datasets'),
    path('datasets/real-world/<int:dataset_id>/', views.RealWorldDataset.as_view(), name='real_world_dataset'),
    path('datasets/synthetic/', views.SyntheticDatasets.as_view(), name='synthetic_datasets'),
    path('datasets/synthetic/<int:dataset_id>/', views.SyntheticDataset.as_view(), name='synthetic_dataset'),

    path('account/application-settings/', views.ApplicationSettings.as_view(), name='application_settings'),
    path('account/datasets/', views.account_datasets, name='account_datasets'),
    path('account/training-datasets/', views.account_training_datasets, name='account_training_datasets'),
    path('account/', views.account, name='account'),

    path('', views.index, name='index'),
]
print(urlpatterns)
