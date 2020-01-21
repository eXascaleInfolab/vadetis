from rest_framework import serializers
from django.core.validators import FileExtensionValidator
from rest_framework.viewsets import ModelViewSet
from vadetisweb.models import DataSet
from vadetisweb.parameters import *


class DatasetSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataSet
        fields = ('title',)


class DatasetChoicesViewSet(ModelViewSet):
    """
    A viewset for viewing and editing dataset instances.
    """
    queryset = DataSet.objects.filter(is_training_data=False)
    serializer = DatasetSerializer(queryset, many=False)


class DatasetUploadSerializer(serializers.ModelSerializer):
    title = serializers.CharField(required=True, max_length=128, help_text='Human readable title of the dataset',
                                  style={'template': 'vadetisweb/parts/input/text_input.html'})

    type = serializers.ChoiceField(choices=DATASET_TYPE, default=REAL_WORLD,
                                   help_text='Determines whether this dataset is real world or synthetic data.',
                                   style={'template': 'vadetisweb/parts/input/select_input.html'})

    csv_file = serializers.FileField(required=True, label='CSV File', help_text='The csv file of the dataset',
                                     validators=[FileExtensionValidator(allowed_extensions=['csv'])],
                                     style={'template': 'vadetisweb/parts/input/text_input.html'})

    type_of_data = serializers.ChoiceField(choices=DATASET_TYPE_OF_DATA, default=SAME_UNITS,
                                           help_text='Same units means that all time series recorded the same unit of values. Choose different units if your features measured in different units.',
                                           style={'template': 'vadetisweb/parts/input/select_input.html'})

    spatial_data = serializers.ChoiceField(choices=DATASET_SPATIAL_DATA, default=NON_SPATIAL,
                                           help_text='Determines whether this dataset is spatial or not. Spatial data requires geographic information about the time series recording location.',
                                           style={'template': 'vadetisweb/parts/input/select_input.html'})

    csv_spatial_file = serializers.FileField(label='Spatial CSV File',
                                             help_text='The csv file of spatial information. It\'s only required if dataset is spatial.',
                                             validators=[FileExtensionValidator(allowed_extensions=['csv'])],
                                             style={'template': 'vadetisweb/parts/input/text_input.html'})

    class Meta:
        model = DataSet
        fields = ('title', 'csv_file', 'type', 'type_of_data', 'spatial_data', 'csv_spatial_file')


class TrainingDatasetUploadSerializer(serializers.ModelSerializer):
    title = serializers.CharField(required=True, max_length=128,
                                  help_text='Human readable title of the training dataset',
                                  style={'template': 'vadetisweb/parts/input/text_input.html'})

    original_dataset = DatasetChoicesViewSet()

    csv_file = serializers.FileField(required=True, label='CSV File', help_text='The csv file of the dataset',
                                     style={'template': 'vadetisweb/parts/input/text_input.html'})

    class Meta:
        model = DataSet
        fields = ('title', 'original_dataset', 'csv_file',)
