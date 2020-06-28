from rest_framework import serializers

from django.urls import reverse

from vadetisweb.fields import DatasetField, DatasetJsonField
from vadetisweb.models import DataSet
from vadetisweb.parameters import REAL_WORLD


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


class DatasetSearchSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField(read_only=True, label="username", many=False)
    display = serializers.SerializerMethodField()
    detection = serializers.SerializerMethodField()

    def get_display(self, obj):
        if obj.type == REAL_WORLD:
            view_link = reverse('vadetisweb:display_real_world_dataset', args=[obj.id])
        else:
            view_link = reverse('vadetisweb:display_synthetic_dataset', args=[obj.id])
        return view_link

    def get_detection(self, obj):
        if obj.type == REAL_WORLD:
            detection_link = reverse('vadetisweb:detection_real_world_dataset', args=[obj.id])
        else:
            detection_link = reverse('vadetisweb:detection_synthetic_dataset', args=[obj.id])
        return detection_link

    class Meta:
        model = DataSet
        fields = ('title', 'owner', 'display', 'detection', )