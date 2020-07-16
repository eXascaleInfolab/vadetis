from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from django.urls import reverse
from django.core.validators import FileExtensionValidator

from vadetisweb.models import DataSet
from vadetisweb.parameters import REAL_WORLD, SYNTHETIC, DATASET_TYPE, BOOLEAN_SELECTION
from vadetisweb.fields import MainDatasetField
from vadetisweb.serializers.account_serializers import UserSerializer


class AccountDatasetDataTablesSerializer(serializers.ModelSerializer):
    title = serializers.CharField(read_only=True)
    timeseries = serializers.SerializerMethodField()
    values = serializers.SerializerMethodField()
    granularity = serializers.CharField(read_only=True)
    spatial = serializers.SerializerMethodField()
    shared = serializers.BooleanField(read_only=True)
    training_datasets = serializers.SerializerMethodField()
    actions = serializers.SerializerMethodField()

    def get_timeseries(self, obj):
        return obj.timeseries_set.count()

    def get_values(self, obj):
        return obj.number_of_dataframe_values()

    def get_spatial(self, obj):
        return obj.is_spatial()

    def get_training_datasets(self, obj):
        return obj.number_of_training_datasets()

    def get_actions(self, obj):
        if obj.type == REAL_WORLD:
            view_link = reverse('vadetisweb:display_real_world_dataset', args=[obj.id])
            detection_link = reverse('vadetisweb:detection_real_world_dataset', args=[obj.id])
            recommendation_link = reverse('vadetisweb:recommendation_real_world_dataset', args=[obj.id])
        else:
            view_link = reverse('vadetisweb:display_synthetic_dataset', args=[obj.id])
            detection_link = reverse('vadetisweb:detection_synthetic_dataset', args=[obj.id])
            recommendation_link = reverse('vadetisweb:recommendation_synthetic_dataset', args=[obj.id])

        edit_link = reverse('vadetisweb:account_dataset_edit', args=[obj.id])

        return '<a href="%s">Display</a> <a href="%s">Detection</a> <a href="%s">Recommendation</a> <a href="%s">Edit</a>' % (
        view_link, detection_link, recommendation_link, edit_link)

    class Meta:
        model = DataSet
        fields = (
            'title', 'timeseries', 'values', 'granularity', 'spatial', 'shared', 'training_datasets', 'actions'
        )


class AccountDatasetSearchSerializer(serializers.Serializer):
    """
        Order is important and must refer to the order in the datatables serializer
    """
    title = serializers.CharField(write_only=True,
                                  style={'template': 'vadetisweb/parts/input/text_input.html',
                                         'class': 'col-lg-3 kt-margin-b-10-tablet-and-mobile',
                                         'input_class': 'search-input',
                                         'col_index': '0'})

    timeseries = serializers.IntegerField(write_only=True,
                                          style={'template': 'vadetisweb/parts/input/text_input.html',
                                                 'input_type': 'number',
                                                 'class': 'col-lg-3 kt-margin-b-10-tablet-and-mobile',
                                                 'input_class': 'search-input',
                                                 'col_index': '1',
                                                 'step': 'any'})

    values = serializers.IntegerField(write_only=True,
                                      style={'template': 'vadetisweb/parts/input/text_input.html',
                                             'input_type': 'number',
                                             'class': 'col-lg-3 kt-margin-b-10-tablet-and-mobile',
                                             'input_class': 'search-input',
                                             'col_index': '2',
                                             'step': 'any'})

    granularity = serializers.CharField(write_only=True,
                                      style={'template': 'vadetisweb/parts/input/text_input.html',
                                             'class': 'col-lg-3 kt-margin-b-10-tablet-and-mobile',
                                             'input_class': 'search-input',
                                             'col_index': '3'})

    spatial = serializers.ChoiceField(write_only=True, choices=BOOLEAN_SELECTION,
                                      style={'template': 'vadetisweb/parts/input/select_input.html',
                                             'class': 'col-lg-3 kt-margin-b-10-tablet-and-mobile',
                                             'input_class': 'search-input',
                                             'col_index': '4'})

    shared = serializers.ChoiceField(write_only=True, choices=BOOLEAN_SELECTION,
                                     style={'template': 'vadetisweb/parts/input/select_input.html',
                                            'class': 'col-lg-3 kt-margin-b-10-tablet-and-mobile',
                                            'input_class': 'search-input',
                                            'col_index': '5'})

    training_datasets = serializers.IntegerField(write_only=True,
                                                 style={'template': 'vadetisweb/parts/input/text_input.html',
                                                        'input_type': 'number',
                                                        'class': 'col-lg-3 kt-margin-b-10-tablet-and-mobile',
                                                        'input_class': 'search-input',
                                                        'col_index': '6'})

    def __init__(self, *args, **kwargs):
        super(AccountDatasetSearchSerializer, self).__init__(*args, **kwargs)


class AccountTrainingDatasetDataTablesSerializer(serializers.ModelSerializer):

    title = serializers.CharField(read_only=True)
    main_dataset = serializers.StringRelatedField(read_only=True, label="Main dataset")
    timeseries = serializers.SerializerMethodField()
    values = serializers.SerializerMethodField()
    granularity = serializers.CharField(read_only=True)
    shared = serializers.BooleanField(read_only=True)
    spatial = serializers.SerializerMethodField()
    actions = serializers.SerializerMethodField(read_only=True)

    def get_timeseries(self, obj):
        return obj.timeseries_set.count()

    def get_values(self, obj):
        return obj.number_of_dataframe_values()

    def get_spatial(self, obj):
        return obj.is_spatial()

    def get_actions(self, obj):
        if obj.type == REAL_WORLD:
            view_link = reverse('vadetisweb:display_real_world_training_dataset', args=[obj.main_dataset.id, obj.id])
        else:
            view_link = reverse('vadetisweb:display_synthetic_training_dataset', args=[obj.main_dataset.id, obj.id])

        edit_link = reverse('vadetisweb:account_training_dataset_edit', args=[obj.id])
        return '<a href="%s">Display</a> <a href="%s">Edit</a>' % (view_link, edit_link)

    class Meta:
        model = DataSet
        fields = (
            'title', 'main_dataset', 'timeseries', 'values', 'granularity', 'spatial', 'shared', 'actions'
        )


class AccountTrainingDatasetSearchSerializer(serializers.Serializer):
    """
        Order is important and must refer to the order in the datatables serializer
    """
    title = serializers.CharField(write_only=True,
                                  style={'template': 'vadetisweb/parts/input/text_input.html',
                                         'class': 'col-lg-3 kt-margin-b-10-tablet-and-mobile',
                                         'input_class': 'search-input',
                                         'col_index': '0'})

    main_dataset = serializers.CharField(write_only=True,
                                         style={'template': 'vadetisweb/parts/input/text_input.html',
                                                'class': 'col-lg-3 kt-margin-b-10-tablet-and-mobile',
                                                'input_class': 'search-input',
                                                'col_index': '1'})

    timeseries = serializers.IntegerField(write_only=True,
                                          style={'template': 'vadetisweb/parts/input/text_input.html',
                                                 'input_type': 'number',
                                                 'class': 'col-lg-3 kt-margin-b-10-tablet-and-mobile',
                                                 'input_class': 'search-input',
                                                 'col_index': '2',
                                                 'step': 'any'})

    values = serializers.IntegerField(write_only=True,
                                      style={'template': 'vadetisweb/parts/input/text_input.html',
                                             'input_type': 'number',
                                             'class': 'col-lg-3 kt-margin-b-10-tablet-and-mobile',
                                             'input_class': 'search-input',
                                             'col_index': '3',
                                             'step': 'any'})

    granularity = serializers.CharField(write_only=True,
                                      style={'template': 'vadetisweb/parts/input/text_input.html',
                                             'class': 'col-lg-3 kt-margin-b-10-tablet-and-mobile',
                                             'input_class': 'search-input',
                                             'col_index': '4'})

    spatial = serializers.ChoiceField(write_only=True, choices=BOOLEAN_SELECTION,
                                      style={'template': 'vadetisweb/parts/input/select_input.html',
                                             'class': 'col-lg-3 kt-margin-b-10-tablet-and-mobile',
                                             'input_class': 'search-input',
                                             'col_index': '5'})

    shared = serializers.ChoiceField(write_only=True, choices=BOOLEAN_SELECTION,
                                     style={'template': 'vadetisweb/parts/input/select_input.html',
                                            'class': 'col-lg-3 kt-margin-b-10-tablet-and-mobile',
                                            'input_class': 'search-input',
                                            'col_index': '6'})

    def __init__(self, *args, **kwargs):
        super(AccountTrainingDatasetSearchSerializer, self).__init__(*args, **kwargs)


class DatasetImportSerializer(serializers.Serializer):
    title = serializers.CharField(required=True, max_length=64, help_text='Human readable title of the dataset',
                                  style={'template': 'vadetisweb/parts/input/text_input.html'})

    csv_file = serializers.FileField(required=True, label='CSV File', help_text='The csv file of the dataset. As anomaly detection is computationally expensive, the dataset must not exceed 100\'000 values.',
                                     validators=[FileExtensionValidator(allowed_extensions=['csv'])],
                                     style={'template': 'vadetisweb/parts/input/file_input.html'})

    owner = UserSerializer(read_only=True, default=serializers.CurrentUserDefault())

    type = serializers.ChoiceField(choices=DATASET_TYPE, default=SYNTHETIC,
                                   help_text='Determines whether this dataset is real world or synthetic data.',
                                   style={'template': 'vadetisweb/parts/input/select_input.html'})

    shared = serializers.BooleanField(default=True, initial=True,
                                      help_text='If shared, this dataset is visible to other users.',
                                      style={'template': 'vadetisweb/parts/input/checkbox_input.html'})

    csv_spatial_file = serializers.FileField(label='Spatial CSV File',
                                             required=False,
                                             allow_empty_file=True,
                                             help_text='The csv file of spatial information. If geographic information about the time series of this dataset is available, you can provide this information here.',
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


class TrainingDatasetImportSerializer(serializers.Serializer):
    title = serializers.CharField(required=True, max_length=128,
                                  help_text='Human readable title of the training dataset',
                                  style={'template': 'vadetisweb/parts/input/text_input.html'})

    owner = UserSerializer(read_only=True, default=serializers.CurrentUserDefault())

    main_dataset = MainDatasetField(label="Main dataset", required=True,
                                    style={'template': 'vadetisweb/parts/input/select_input.html'})

    shared = serializers.BooleanField(default=True, initial=True,
                                      help_text='If shared, this training dataset is visible to other users.',
                                      style={'template': 'vadetisweb/parts/input/checkbox_input.html'})

    csv_file = serializers.FileField(required=True, label='CSV File', help_text='The csv file of the dataset. As anomaly detection is computationally expensive, the dataset must not exceed 10\'000 values.',
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


class AccountDatasetUpdateSerializer(serializers.ModelSerializer):
    title = serializers.CharField(required=True, max_length=64, help_text='Human readable title of the dataset',
                                  style={'template': 'vadetisweb/parts/input/text_input.html'})

    type = serializers.ChoiceField(choices=DATASET_TYPE, default=SYNTHETIC,
                                   help_text='Specify whether this dataset is real-world or synthetic data. Note: Main datasets and their training data share the same type and get updated as well.',
                                   style={'template': 'vadetisweb/parts/input/select_input.html',
                                          'help_text_in_popover': False})

    shared = serializers.BooleanField(required=True, help_text='If shared, this dataset is visible to other users.',
                                      style={'template': 'vadetisweb/parts/input/checkbox_input.html'})

    class Meta:
        model = DataSet
        fields = ('title', 'type', 'shared')


class AccountDatasetDeleteSerializer(serializers.Serializer):
    confirm = serializers.BooleanField(required=True,
                                       label="Confirm",
                                       help_text='Check to delete this dataset',
                                       style={'template': 'vadetisweb/parts/input/checkbox_input.html'})
