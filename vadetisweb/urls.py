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
router.register(r'account/datasets', views.AccountDatasetDataTableViewSet, basename='account_datasets_datatable')
router.register(r'account/training-datasets', views.AccountTrainingDatasetDataTableViewSet, basename='account_training_datasets_datatable')
router.register(r'display/datasets/synthetic', views.DisplaySyntheticDatasetDataTableViewSet, basename='display_synthetic_datasets_datatable')
router.register(r'display/datasets/real-world', views.DisplayRealWorldDatasetDataTableViewSet, basename='display_real_world_datasets_datatable')
router.register(r'display/training-datasets', views.DisplayTrainingDatasetDataTableViewSet, basename='display_training_datasets_datatable')
router.register(r'detection/datasets/synthetic', views.DetectionSyntheticDatasetDataTableViewSet, basename='detection_synthetic_datasets_datatable')
router.register(r'detection/datasets/real-world', views.DetectionRealWorldDatasetDataTableViewSet, basename='detection_real_world_datasets_datatable')
router.register(r'suggestion/datasets/synthetic', views.SuggestionSyntheticDatasetDataTableViewSet, basename='suggestion_synthetic_datasets_datatable')
router.register(r'suggestion/datasets/real-world', views.SuggestionRealWorldDatasetDataTableViewSet, basename='suggestion_real_world_datasets_datatable')

apipatterns = [
    path('api/', include((router.urls))),
    path('api/detection/<int:dataset_id>/', views.DetectionAlgorithmSelectionView.as_view(), name='detection_algorithm_selection'),
    path('api/detection/<int:dataset_id>/lisa/pearson', views.DetectionLisaPearson.as_view(), name='detection_lisa_person'),
    path('api/detection/<int:dataset_id>/lisa/dtw-pearson', views.DetectionLisaDtwPearson.as_view(), name='detection_lisa_dtw_person'),
    path('api/detection/<int:dataset_id>/lisa/geo', views.DetectionLisaGeoDistance.as_view(), name='detection_lisa_geo'),
    path('api/detection/<int:dataset_id>/rpca/mestimator', views.DetectionRPCAMEstimatorLoss.as_view(), name='detection_rpca_mestimator'),
    path('api/detection/<int:dataset_id>/histogram', views.DetectionHistogram.as_view(), name='detection_histogram'),
    path('api/detection/<int:dataset_id>/cluster', views.DetectionCluster.as_view(), name='detection_cluster'),
    path('api/detection/<int:dataset_id>/svm', views.DetectionSVM.as_view(), name='detection_svm'),
    path('api/detection/<int:dataset_id>/isolationforest', views.DetectionIsolationForest.as_view(), name='detection_isolation_forest'),

    path('api/injection/<int:dataset_id>/', views.InjectionView.as_view(), name='injection_anomaly'),

    path('api/suggestion/<int:dataset_id>/', views.SuggestionView.as_view(), name='suggestion_scores'),

    path('api/dataset/<int:dataset_id>/', views.DatasetJson.as_view(), name='dataset_json'),
    path('api/dataset/<int:dataset_id>/update/', views.AccountDatasetUpdate.as_view(), name='account_dataset_update'),
    path('api/dataset/<int:dataset_id>/delete/', views.AccountDatasetDelete.as_view(), name='account_dataset_delete'),
    path('api/training-dataset/<int:dataset_id>/update/', views.AccountTrainingDatasetUpdate.as_view(), name='account_training_dataset_update'),
    path('api/training-dataset/<int:dataset_id>/delete/', views.AccountTrainingDatasetDelete.as_view(), name='account_training_dataset_delete'),

    path('api/dataset/search/', views.DatasetSearchView.as_view(), name='dataset_search'),
    path('api/dataset/download/', views.DatasetFileDownload.as_view(), name='dataset_download_file'),

    path('api/portlet/image/', views.ImagePortlet.as_view(), name='image_portlet'),
    path('api/portlet/score/', views.ScorePortlet.as_view(), name='score_portlet'),
    path('api/portlet/suggestion/', views.SuggestionPortlet.as_view(), name='suggestion_portlet'),
    path('api/portlet/threshold/', views.ThresholdFormPortlet.as_view(), name='threshold_portlet'),
    path('api/portlet/injection/<int:dataset_id>/', views.InjectionFormPortlet.as_view(), name='injection_form_portlet'),

    path('api/threshold-update', views.DatasetThresholdUpdateJson.as_view(), name='threshold_update_json'),
    path('api/image/cnf/', views.CnfImage.as_view(), name='cnf_image'),
    path('api/image/thresholds-scores/', views.ThresholdsScoresImage.as_view(), name='thresholds_scores_image'),

    path('api/locations/<int:dataset_id>/', views.DatasetLocationsJson.as_view(), name='dataset_locations'),
]

urlpatterns = apipatterns + [

    path('account/datasets/upload/', views.AccountUploadDataset.as_view(), name='account_datasets_upload'),
    path('account/training-datasets/upload/', views.AccountUploadTrainingDataset.as_view(), name='account_training_datasets_upload'),

    path('display/real-world/', views.DisplayRealWorldDatasets.as_view(), name='display_real_world_datasets'),
    path('display/real-world/<int:dataset_id>/', views.DisplayRealWorldDataset.as_view(), name='display_real_world_dataset'),
    path('display/real-world/<int:dataset_id>/<int:training_dataset_id>/', views.DisplayRealWorldTrainingDataset.as_view(), name='display_real_world_training_dataset'),
    path('display/synthetic/', views.DisplaySyntheticDatasets.as_view(), name='display_synthetic_datasets'),
    path('display/synthetic/<int:dataset_id>/', views.DisplaySyntheticDataset.as_view(), name='display_synthetic_dataset'),
    path('display/synthetic/<int:dataset_id>/<int:training_dataset_id>/', views.DisplaySyntheticTrainingDataset.as_view(), name='display_synthetic_training_dataset'),

    path('detection/real-world/', views.DetectionRealWorldDatasets.as_view(), name='detection_real_world_datasets'),
    path('detection/real-world/<int:dataset_id>/', views.DetectionRealWorldDataset.as_view(), name='detection_real_world_dataset'),
    path('detection/synthetic/', views.DetectionSyntheticDatasets.as_view(), name='detection_synthetic_datasets'),
    path('detection/synthetic/<int:dataset_id>/', views.DetectionSyntheticDataset.as_view(), name='detection_synthetic_dataset'),

    path('suggestion/real-world/', views.SuggestionRealWorldDatasets.as_view(), name='suggestion_real_world_datasets'),
    path('suggestion/real-world/<int:dataset_id>/', views.SuggestionRealWorldDataset.as_view(), name='suggestion_real_world_dataset'),
    path('suggestion/synthetic/', views.SuggestionSyntheticDatasets.as_view(), name='suggestion_synthetic_datasets'),
    path('suggestion/synthetic/<int:dataset_id>/', views.SuggestionSyntheticDataset.as_view(), name='suggestion_synthetic_dataset'),

    path('account/application-setting/', views.ApplicationSetting.as_view(), name='application_setting'),
    path('account/datasets/', views.account_datasets, name='account_datasets'),
    path('account/datasets/<int:dataset_id>/edit/', views.AccountDatasetEdit.as_view(), name='account_dataset_edit'),
    path('account/training-datasets/<int:dataset_id>/edit/', views.AccountTrainingDatasetEdit.as_view(), name='account_training_dataset_edit'),
    path('account/training-datasets/', views.account_training_datasets, name='account_training_datasets'),
    path('account/user/update', views.AccountUserUpdate.as_view(), name='account_user_update'),
    path('account/pwd/update', views.AccountPasswordUpdate.as_view(), name='account_pwd_update'),
    path('account/social/update', views.AccountSocialDisconnectUpdate.as_view(), name='account_social_disconnect_update'),
    path('account/delete', views.AccountDelete.as_view(), name='account_delete'),
    path('account/', views.account, name='account'),


    path('about/', views.about, name='about'),
    path('', views.index, name='index'),
]
