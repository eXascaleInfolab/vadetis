from rest_framework import serializers
from django.core.validators import FileExtensionValidator
from rest_framework.validators import UniqueTogetherValidator

from vadetisweb.models import DataSet, User
from vadetisweb.parameters import *
from vadetisweb.fields import UserOriginalDatasetField

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username',)


class DatasetImportSerializer(serializers.Serializer):
    title = serializers.CharField(required=True, max_length=128, help_text='Human readable title of the dataset',
                                  style={'template': 'vadetisweb/parts/input/text_input.html'})

    csv_file = serializers.FileField(required=True, label='CSV File', help_text='The csv file of the dataset',
                                     validators=[FileExtensionValidator(allowed_extensions=['csv'])],
                                     style={'template': 'vadetisweb/parts/input/text_input.html'})

    owner = UserSerializer(read_only=True, default=serializers.CurrentUserDefault())

    type = serializers.ChoiceField(choices=DATASET_TYPE, default=REAL_WORLD,
                                   help_text='Determines whether this dataset is real world or synthetic data.',
                                   style={'template': 'vadetisweb/parts/input/select_input.html'})

    spatial_data = serializers.ChoiceField(choices=DATASET_SPATIAL_DATA, default=NON_SPATIAL,
                                           help_text='Determines whether this dataset is spatial or not. Spatial data requires geographic information about the time series recording location.',
                                           style={'template': 'vadetisweb/parts/input/select_input.html'})

    csv_spatial_file = serializers.FileField(label='Spatial CSV File',
                                             required=False,
                                             allow_empty_file=True,
                                             help_text='The csv file of spatial information. It\'s only required if dataset is spatial.',
                                             validators=[FileExtensionValidator(allowed_extensions=['csv'])],
                                             style={'template': 'vadetisweb/parts/input/text_input.html'})

    class Meta:
        validators = [
            UniqueTogetherValidator(
                queryset=DataSet.objects.all(),
                fields=['title', 'owner'],
                message='You already have a dataset with this title. Title and owner of a dataset must be distinct.'
            )
        ]

    def validate(self, data):
        """
        Object level validation
        """
        if data['spatial_data'] == SPATIAL and data['csv_spatial_file'] is None:
            raise serializers.ValidationError("A spatial dataset requires a CSV file about location information.")
        return data


class TrainingDatasetImportSerializer(serializers.Serializer):
    title = serializers.CharField(required=True, max_length=128,
                                  help_text='Human readable title of the training dataset',
                                  style={'template': 'vadetisweb/parts/input/text_input.html'})

    owner = UserSerializer(read_only=True, default=serializers.CurrentUserDefault())

    original_dataset = UserOriginalDatasetField(label="Associated dataset", required=True)

    csv_file = serializers.FileField(required=True, label='CSV File', help_text='The csv file of the dataset',
                                     style={'template': 'vadetisweb/parts/input/text_input.html'})

    class Meta:
        validators = [
            UniqueTogetherValidator(
                queryset=DataSet.objects.all(),
                fields=['title', 'owner'],
                message='You already have a dataset with this title. Title and owner of a dataset must be distinct.'
            )
        ]


class DatasetDataTablesSerializer(serializers.ModelSerializer):
    title = serializers.CharField(read_only=True)

    class Meta:
        model = DataSet
        fields = (
            'title',
        )
