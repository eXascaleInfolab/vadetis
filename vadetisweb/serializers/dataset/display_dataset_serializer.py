import numpy as np
from django.urls import reverse
from rest_framework import serializers

from vadetisweb.models import DataSet
from vadetisweb.parameters import *


class DisplayDatasetDataTablesSerializer(serializers.ModelSerializer):

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
            link = reverse('vadetisweb:display_real_world_dataset', args=[obj.id])
        else:
            link = reverse('vadetisweb:display_synthetic_dataset', args=[obj.id])
        return '<a href="%s">View</a>' % (link)

    class Meta:
        model = DataSet
        fields = (
            'title', 'owner', 'timeseries', 'values', 'frequency', 'spatial_data', 'training_datasets', 'actions'
        )


class DisplayDatasetSearchSerializer(serializers.Serializer):
    """
        Order is important and must refer to the order in the datatables serializer
    """
    title = serializers.CharField(write_only=True,
                                  style={'template': 'vadetisweb/parts/input/text_input.html',
                                         'class': 'col-lg-3 kt-margin-b-10-tablet-and-mobile',
                                         'input_class' : 'search-input',
                                         'col_index' : '0' })

    owner = serializers.CharField(write_only=True,
                                  style={'template': 'vadetisweb/parts/input/text_input.html',
                                         'class': 'col-lg-3 kt-margin-b-10-tablet-and-mobile',
                                         'input_class': 'search-input',
                                         'col_index': '1'})

    timeseries = serializers.IntegerField(write_only=True,
                                          style={'template': 'vadetisweb/parts/input/text_input.html',
                                                 'input_type': 'number',
                                                 'class': 'col-lg-3 kt-margin-b-10-tablet-and-mobile',
                                                 'input_class' : 'search-input',
                                                 'col_index': '2',
                                                 'step': 'any'})

    values = serializers.IntegerField(write_only=True,
                                      style={'template': 'vadetisweb/parts/input/text_input.html',
                                             'input_type' : 'number',
                                             'class': 'col-lg-3 kt-margin-b-10-tablet-and-mobile',
                                             'input_class': 'search-input',
                                             'col_index': '3',
                                             'step': 'any'})

    frequency = serializers.CharField(write_only=True,
                                      style={'template': 'vadetisweb/parts/input/text_input.html',
                                             'class': 'col-lg-3 kt-margin-b-10-tablet-and-mobile',
                                             'input_class' : 'search-input',
                                             'col_index' : '4' })

    spatial = serializers.ChoiceField(write_only=True, choices=BOOLEAN_SELECTION,
                                      style={'template': 'vadetisweb/parts/input/select_input.html',
                                             'class': 'col-lg-3 kt-margin-b-10-tablet-and-mobile',
                                             'input_class' : 'search-input',
                                             'col_index' : '5' })

    public = serializers.ChoiceField(write_only=True, choices=BOOLEAN_SELECTION,
                                     style={'template': 'vadetisweb/parts/input/select_input.html',
                                            'class': 'col-lg-3 kt-margin-b-10-tablet-and-mobile',
                                            'input_class' : 'search-input',
                                            'col_index' : '6' })

    training_datasets = serializers.IntegerField(write_only=True,
                                                 style={'template': 'vadetisweb/parts/input/text_input.html',
                                                        'input_type': 'number',
                                                        'class': 'col-lg-3 kt-margin-b-10-tablet-and-mobile',
                                                        'input_class' : 'search-input',
                                                        'col_index' : '7'})

    def __init__(self, *args, **kwargs):
        super(DisplayDatasetSearchSerializer, self).__init__(*args, **kwargs)