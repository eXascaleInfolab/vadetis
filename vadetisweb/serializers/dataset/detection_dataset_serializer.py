import numpy as np
from django.urls import reverse
from rest_framework import serializers

from vadetisweb.models import DataSet
from vadetisweb.parameters import *


class DetectionDatasetDataTablesSerializer(serializers.ModelSerializer):
    title = serializers.CharField(read_only=True)
    owner = serializers.CharField(read_only=True)
    timeseries = serializers.SerializerMethodField()
    values = serializers.SerializerMethodField()
    frequency = serializers.CharField(read_only=True)
    spatial_data = serializers.SerializerMethodField()
    training_datasets = serializers.SerializerMethodField()
    actions = serializers.SerializerMethodField()

    def get_timeseries(self, obj):
        return obj.timeseries_set.count()

    def get_values(self, obj):
        np_num_values = obj.dataframe.count().sum()
        return int(np_num_values) if isinstance(np_num_values, np.integer) else np_num_values

    def get_spatial_data(self, obj):
        return all(ts.location is not None for ts in obj.timeseries_set.all())

    def get_training_datasets(self, obj):
        return obj.training_dataset.count()

    def get_actions(self, obj):
        if obj.type == REAL_WORLD:
            link = reverse('vadetisweb:detection_real_world_dataset', args=[obj.id])
        else:
            link = reverse('vadetisweb:detection_synthetic_dataset', args=[obj.id])
        return '<a href="%s">View</a>' % (link)

    class Meta:
        model = DataSet
        fields = (
            'title', 'owner', 'timeseries', 'values', 'frequency', 'spatial_data', 'training_datasets', 'actions'
        )