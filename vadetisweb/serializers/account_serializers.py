import numpy as np
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from django.core.validators import MaxLengthValidator, MaxValueValidator, MinValueValidator, RegexValidator, FileExtensionValidator
from django.urls import reverse

from vadetisweb.models import UserSettings, DataSet, User
from vadetisweb.parameters import REAL_WORLD, DATASET_TYPE, DATASET_SPATIAL_DATA, NON_SPATIAL, SPATIAL
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
                                     style={'template': 'vadetisweb/parts/input/file_input.html'})

    owner = UserSerializer(read_only=True, default=serializers.CurrentUserDefault())

    type = serializers.ChoiceField(choices=DATASET_TYPE, default=REAL_WORLD,
                                   help_text='Determines whether this dataset is real world or synthetic data.',
                                   style={'template': 'vadetisweb/parts/input/select_input.html'})

    is_public = serializers.BooleanField(default=True,
                                         help_text='Determines if this dataset is available to other users',
                                         style={'template': 'vadetisweb/parts/input/checkbox_input.html'})

    spatial_data = serializers.ChoiceField(choices=DATASET_SPATIAL_DATA, default=NON_SPATIAL,
                                           help_text='Determines whether this dataset is spatial or not. Spatial data requires geographic information about the time series recording location.',
                                           style={'template': 'vadetisweb/parts/input/select_input.html'})

    csv_spatial_file = serializers.FileField(label='Spatial CSV File',
                                             required=False,
                                             allow_empty_file=True,
                                             help_text='The csv file of spatial information. It\'s only required if dataset is spatial.',
                                             validators=[FileExtensionValidator(allowed_extensions=['csv'])],
                                             style={'template': 'vadetisweb/parts/input/file_input.html'})

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

    original_dataset = UserOriginalDatasetField(label="Associated dataset", required=True,
                                   style={'template': 'vadetisweb/parts/input/select_input.html'})

    is_public = serializers.BooleanField(default=True,
                                         help_text='Determines if this dataset is available to other users',
                                         style={'template': 'vadetisweb/parts/input/checkbox_input.html'})

    csv_file = serializers.FileField(required=True, label='CSV File', help_text='The csv file of the dataset',
                                     style={'template': 'vadetisweb/parts/input/file_input.html'})

    class Meta:
        validators = [
            UniqueTogetherValidator(
                queryset=DataSet.objects.all(),
                fields=['title', 'owner'],
                message='You already have a dataset with this title. Title and owner of a dataset must be distinct.'
            )
        ]


class UserSettingsSerializer(serializers.ModelSerializer):
    """
    The form for the settings of the user
    """

    highcharts_height = serializers.IntegerField(default=500,
                                                 help_text='Value in pixels, Default: 500',
                                                 validators=[MinValueValidator(250)],
                                                 style={'template': 'vadetisweb/parts/input/text_input.html'})

    legend_height = serializers.IntegerField(default=100,
                                             help_text='Value in pixels, Default: 100',
                                             validators=[MinValueValidator(50)],
                                             style={'template': 'vadetisweb/parts/input/text_input.html'})

    color_outliers = serializers.CharField(max_length=7, default="#FF0000",
                                           help_text='Default: #FF0000, the RGB color used to mark outliers',
                                           validators=[RegexValidator(regex='^#(?:[0-9a-fA-F]{3}){1,2}$')],
                                           style={'template': 'vadetisweb/parts/input/text_input.html',
                                                  'input_type': 'color'})

    color_clusters = serializers.CharField(max_length=7, default="#0000FF",
                                           help_text='Default: #0000FF, the RGB color used to mark LISA clusters of high or low values',
                                           validators=[RegexValidator(regex='^#(?:[0-9a-fA-F]{3}){1,2}$')],
                                           style={'template': 'vadetisweb/parts/input/text_input.html',
                                                  'input_type': 'color'})

    color_true_positive = serializers.CharField(max_length=7, default="#008800",
                                                help_text='Default: #008800, the RGB color used to mark true positives',
                                                validators=[RegexValidator(regex='^#(?:[0-9a-fA-F]{3}){1,2}$')],
                                                style={'template': 'vadetisweb/parts/input/text_input.html',
                                                       'input_type': 'color'})

    color_false_positive = serializers.CharField(max_length=7, default="#FF0000",
                                                 help_text='Default: #FF0000, the RGB color used to mark false positives',
                                                 validators=[RegexValidator(regex='^#(?:[0-9a-fA-F]{3}){1,2}$')],
                                                 style={'template': 'vadetisweb/parts/input/text_input.html',
                                                        'input_type': 'color'})

    color_false_negative = serializers.CharField(max_length=7, default="#0000FF",
                                                 help_text='Default: #0000FF, the RGB color used to mark false negatives',
                                                 validators=[RegexValidator(regex='^#(?:[0-9a-fA-F]{3}){1,2}$')],
                                                 style={'template': 'vadetisweb/parts/input/text_input.html',
                                                        'input_type': 'color'})

    round_digits = serializers.IntegerField(default=3,
                                            help_text='Must be a number between 1 and 6',
                                            validators=[MinValueValidator(1), MaxValueValidator(6)],
                                            style={'template': 'vadetisweb/parts/input/text_input.html',
                                                   'class': 'form-group-last'})

    class Meta:
        model = UserSettings
        fields = ('highcharts_height', 'legend_height', 'color_outliers', 'color_clusters',
                  'color_true_positive', 'color_false_positive', 'color_false_negative', 'round_digits')


class AccountDatasetDataTablesSerializer(serializers.ModelSerializer):
    title = serializers.CharField(read_only=True)
    owner = serializers.CharField(read_only=True)
    timeseries = serializers.SerializerMethodField()
    values = serializers.SerializerMethodField()
    frequency = serializers.CharField(read_only=True)
    spatial_data = serializers.BooleanField(read_only=True)
    is_public = serializers.BooleanField(read_only=True)
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
            'title', 'owner', 'timeseries', 'values', 'frequency', 'spatial_data', 'is_public', 'training_datasets', 'actions'
        )


class AccountTrainingDatasetDataTablesSerializer(serializers.ModelSerializer):
    title = serializers.CharField(read_only=True)
    owner = serializers.CharField(read_only=True)
    timeseries = serializers.SerializerMethodField()
    values = serializers.SerializerMethodField()
    frequency = serializers.CharField(read_only=True)
    is_public = serializers.BooleanField(read_only=True)
    spatial_data = serializers.BooleanField(read_only=True)

    def get_timeseries(self, obj):
        return obj.timeseries_set.count()

    def get_values(self, obj):
        np_num_values = obj.dataframe.count().sum()
        return int(np_num_values) if isinstance(np_num_values, np.integer) else np_num_values

    class Meta:
        model = DataSet
        fields = (
            'title', 'owner', 'timeseries', 'values', 'frequency', 'is_public', 'spatial_data',
        )
