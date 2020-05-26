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
router.register(r'account/datasets', views.DatasetDataTableViewSet, basename='account_datasets_datatable')
router.register(r'account/training-datasets', views.TrainingDatasetDataTableViewSet, basename='account_training_datasets_datatable')
router.register(r'datasets/synthetic', views.SyntheticDatasetDataTableViewSet, basename='synthetic_datasets_datatable')
router.register(r'datasets/real-world', views.RealWorldDatasetDataTableViewSet, basename='real_world_datasets_datatable')

apipatterns = [
    path('api/', include((router.urls))),
    path('api/anomaly-detection/<int:dataset_id>/', views.AnomalyDetectionAlgorithmSelectionView.as_view(), name='anomaly_detection_algorithm_selection'),
    path('api/anomaly-detection/<int:dataset_id>/lisa/pearson', views.AnomalyDetectionLisaPearson.as_view(), name='anomaly_detection_lisa_person'),
    path('api/anomaly-detection/<int:dataset_id>/lisa/dtw-pearson', views.AnomalyDetectionLisaDtwPearson.as_view(), name='anomaly_detection_lisa_dtw_person'),
    path('api/anomaly-detection/<int:dataset_id>/lisa/geo', views.AnomalyDetectionLisaGeoDistance.as_view(), name='anomaly_detection_lisa_geo'),
    path('api/anomaly-detection/<int:dataset_id>/rpca/mestimator', views.AnomalyDetectionRPCAMEstimatorLoss.as_view(), name='anomaly_detection_rpca_mestimator'),
    path('api/anomaly-detection/<int:dataset_id>/histogram', views.AnomalyDetectionHistogram.as_view(), name='anomaly_detection_histogram'),
    path('api/anomaly-detection/<int:dataset_id>/cluster', views.AnomalyDetectionCluster.as_view(), name='anomaly_detection_cluster'),
    path('api/anomaly-detection/<int:dataset_id>/svm', views.AnomalyDetectionSVM.as_view(), name='anomaly_detection_svm'),
    path('api/anomaly-detection/<int:dataset_id>/isolationforest', views.AnomalyDetectionIsolationForest.as_view(), name='anomaly_detection_isolation_forest'),

    path('api/anomaly-detection/<int:dataset_id>/json/', views.DatasetJsonPerformAnomalyDetectionJson.as_view(),
         name='anomaly_detection_json'),

    path('api/anomaly-injection/<int:dataset_id>/', views.AnomalyInjectionFormView.as_view(), name='anomaly_injection_form'),
    path('api/dataset/<int:dataset_id>/', views.DatasetJson.as_view(), name='dataset_json'),
    path('api/dataset/<int:dataset_id>/update/', views.DatasetUpdateJson.as_view(), name='dataset_update_json'),
    path('api/datasets/<int:dataset_id>/perform/', views.DatasetPerformAnomalyDetectionJson.as_view(),
         name='dataset_perform_anomaly_detection_json'),
    path('api/threshold-update', views.DatasetThresholdUpdateJson.as_view(), name='threshold_update_json'),
    path('api/image/cnf/', views.CnfImage.as_view(), name='cnf_image'),
    path('api/image/thresholds-scores/', views.ThresholdsScoresImage.as_view(), name='thresholds_scores_image'),
]

urlpatterns = apipatterns + [

    path('account/datasets/upload/', views.AccountUploadDataset.as_view(), name='account_datasets_upload'),
    path('account/training-datasets/upload/', views.AccountUploadTrainingDataset.as_view(), name='account_training_datasets_upload'),

    path('datasets/real-world/', views.RealWorldDatasets.as_view(), name='real_world_datasets'),
    path('datasets/real-world/<int:dataset_id>/', views.RealWorldDataset.as_view(), name='real_world_dataset'),
    path('datasets/synthetic/', views.SyntheticDatasets.as_view(), name='synthetic_datasets'),
    path('datasets/synthetic/<int:dataset_id>/', views.SyntheticDataset.as_view(), name='synthetic_dataset'),
    path('datasets/synthetic/<int:dataset_id>/perform', views.SyntheticDatasetPerformAnomalyDetection.as_view(), name='synthetic_dataset_perform'),

    path('account/application-setting/', views.ApplicationSetting.as_view(), name='application_setting'),
    path('account/datasets/', views.account_datasets, name='account_datasets'),
    path('account/training-datasets/', views.account_training_datasets, name='account_training_datasets'),
    path('account/', views.account, name='account'),

    path('', views.index, name='index'),
]
