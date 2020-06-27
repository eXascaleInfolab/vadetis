from rest_framework import serializers

from vadetisweb.fields import DatasetField, DatasetJsonField


class DatasetExportSerializer(serializers.Serializer):
    dataset_series_json = DatasetJsonField(initial=None, binary=False, encoder=None,
                                           style={'template': 'vadetisweb/parts/input/hidden_input.html',
                                                  'id': 'dataset_series_json'})

    def __init__(self, *args, **kwargs):
        super(DatasetExportSerializer, self).__init__(*args, **kwargs)


class DatasetUpdateSerializer(serializers.Serializer):
    dataset = DatasetField(default='overridden')
    dataset_series_json = DatasetJsonField(initial=None, binary=False, encoder=None,
                                           style={'template': 'vadetisweb/parts/input/hidden_input.html',
                                                  'id': 'dataset_series_json'})

    def __init__(self, *args, **kwargs):
        super(DatasetUpdateSerializer, self).__init__(*args, **kwargs)