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
    spatial = serializers.SerializerMethodField()
    training_datasets = serializers.SerializerMethodField()
    actions = serializers.SerializerMethodField()

    def get_timeseries(self, obj):
        return obj.timeseries_set.count()

    def get_values(self, obj):
        return obj.number_of_dataframe_values()

    def get_spatial(self, obj):
        return obj.is_spatial()

    def get_training_datasets(self, obj):
        return obj.number_of_public_training_datasets()

    def get_actions(self, obj):
        if obj.type == REAL_WORLD:
            link = reverse('vadetisweb:display_real_world_dataset', args=[obj.id])
        else:
            link = reverse('vadetisweb:display_synthetic_dataset', args=[obj.id])
        return '<a href="%s">Display</a>' % (link)

    class Meta:
        model = DataSet
        fields = (
            'title', 'owner', 'timeseries', 'values', 'frequency', 'spatial', 'training_datasets', 'actions'
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

    training_datasets = serializers.IntegerField(write_only=True,
                                                 style={'template': 'vadetisweb/parts/input/text_input.html',
                                                        'input_type': 'number',
                                                        'class': 'col-lg-3 kt-margin-b-10-tablet-and-mobile',
                                                        'input_class' : 'search-input',
                                                        'col_index' : '6'})

    def __init__(self, *args, **kwargs):
        super(DisplayDatasetSearchSerializer, self).__init__(*args, **kwargs)


class DisplayTrainingDatasetDataTablesSerializer(serializers.ModelSerializer):

    title = serializers.CharField(read_only=True)
    values = serializers.SerializerMethodField()
    actions = serializers.SerializerMethodField()

    def get_values(self, obj):
        return obj.number_of_dataframe_values()

    def get_actions(self, obj):
        if obj.type == REAL_WORLD:
            link = reverse('vadetisweb:display_real_world_training_dataset', args=[obj.main_dataset.id, obj.id])
        else:
            link = reverse('vadetisweb:display_synthetic_training_dataset', args=[obj.main_dataset.id, obj.id])
        return '<a href="%s">Display</a>' % (link)

    class Meta:
        model = DataSet
        fields = (
            'title', 'values', 'actions'
        )