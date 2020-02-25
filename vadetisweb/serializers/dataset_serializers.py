import numpy as np
from rest_framework import serializers

from django.urls import reverse

from vadetisweb.models import DataSet, User
from vadetisweb.parameters import *

class DatasetDataTablesSerializer(serializers.ModelSerializer):
    title = serializers.CharField(read_only=True)
    owner = serializers.CharField(read_only=True)
    timeseries = serializers.SerializerMethodField()
    values = serializers.SerializerMethodField()
    frequency = serializers.CharField(read_only=True)
    spatial_data = serializers.BooleanField(read_only=True)
    training_datasets = serializers.SerializerMethodField()
    actions = serializers.SerializerMethodField()

    def get_timeseries(self, obj):
        return obj.timeseries_set.count()

    def get_values(self, obj):
        np_num_values = obj.dataframe.count().sum()
        return int(np_num_values) if isinstance(np_num_values, np.integer) else np_num_values

    def get_training_datasets(self, obj):
        return obj.training_dataset.count()

    def get_actions(self, obj):
        if obj.type == REAL_WORLD:
            link = reverse('vadetisweb:real_world_dataset', args=[obj.id])
        else:
            link = reverse('vadetisweb:synthetic_dataset', args=[obj.id])
        return '<a href="%s">View</a>' % (link)

    class Meta:
        model = DataSet
        fields = (
            'title', 'owner', 'timeseries', 'values', 'frequency', 'spatial_data', 'training_datasets', 'actions'
        )


class TrainingDatasetDataTablesSerializer(serializers.ModelSerializer):
    title = serializers.CharField(read_only=True)
    owner = serializers.CharField(read_only=True)
    timeseries = serializers.SerializerMethodField()
    values = serializers.SerializerMethodField()
    frequency = serializers.CharField(read_only=True)
    spatial_data = serializers.BooleanField(read_only=True)

    def get_timeseries(self, obj):
        return obj.timeseries_set.count()

    def get_values(self, obj):
        np_num_values = obj.dataframe.count().sum()
        return int(np_num_values) if isinstance(np_num_values, np.integer) else np_num_values

    class Meta:
        model = DataSet
        fields = (
            'title', 'owner', 'timeseries', 'values', 'frequency', 'spatial_data',
        )
