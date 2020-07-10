from rest_framework import serializers

from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist

from vadetisweb.parameters import TIME_RANGE, ANOMALY_DETECTION_SCORE_TYPES
from vadetisweb.models import DataSet, TimeSeries
from vadetisweb.utils.request_utils import q_public_or_user_is_owner, q_related_public_or_user_is_owner


class DatasetField(serializers.HiddenField):
    """
        Note: a HiddenField should normally not be used that way (overriding default value),
        but its the most comfortable way to have a write only field that is excluded from frontend serializing
    """

    def get_value(self, dictionary):
        dataset_selected = self.context.get('dataset_selected', None)
        request = self.context.get('request', None)
        if dataset_selected is not None and request is not None:
            dataset = DataSet.objects.filter(Q(id=dataset_selected, training_data=False),
                                             q_public_or_user_is_owner(request)).first()
            if dataset is None:
                raise ObjectDoesNotExist
            return dataset
        else:
            raise ObjectDoesNotExist


class TrainingDatasetField(serializers.PrimaryKeyRelatedField):
    def __init__(self, **kwargs):
        super(TrainingDatasetField, self).__init__(**kwargs)
        self.help_text = "The dataset used to train the anomaly detection model."
        self.style = {'template': 'vadetisweb/parts/input/select_input.html',
                      'help_text_in_popover': True}

    def get_queryset(self):
        dataset_selected = self.context.get('dataset_selected', None)
        request = self.context.get('request', None)
        if dataset_selected is not None and request is not None:
            return DataSet.objects.filter(Q(main_dataset__id=dataset_selected, training_data=True),
                                          q_public_or_user_is_owner(request))

        return DataSet.objects.none()

    def display_value(self, instance):
        return instance.title


class TimeSeriesField(serializers.PrimaryKeyRelatedField):
    def __init__(self, **kwargs):
        super(TimeSeriesField, self).__init__(**kwargs)
        self.style = {'template': 'vadetisweb/parts/input/select_input.html',
                      'help_text_in_popover': True}

    def get_queryset(self):
        dataset_selected = self.context.get('dataset_selected', None)
        request = self.context.get('request', None)
        # timeseries_selected = self.context.get('timeseries_selected', None)
        if dataset_selected is not None and request is not None:
            return TimeSeries.objects.filter(Q(datasets__in=[dataset_selected]),
                                             q_related_public_or_user_is_owner(request))
        return TimeSeries.objects.none()

    def display_value(self, instance):
        return instance.name


class TrainSizeFloatField(serializers.FloatField):
    def __init__(self, **kwargs):
        super(TrainSizeFloatField, self).__init__(**kwargs)
        self.label = 'Train Size'
        self.help_text = 'Represent the proportion of the training dataset to use for model training. The rest of the data will be used to validate the model. At least 20% of the data will be required to either train or validate the model.'
        self.style = {'template': 'vadetisweb/parts/input/ion_slider_input.html',
                      'id': 'train_size',
                      'data_type': "single",
                      'data_grid': "true",
                      'data_min': self.min_value,
                      'data_max': self.max_value,
                      'data_from': self.initial,
                      'data_step': "0.01",
                      'help_text_in_popover': True}


class WindowSizeIntegerField(serializers.IntegerField):
    def __init__(self, **kwargs):
        super(WindowSizeIntegerField, self).__init__(**kwargs)
        self.label = 'Window Size'
        self.help_text = 'Select the size of the moving window to compute the correlation between the time series.'
        self.style = {'template': 'vadetisweb/parts/input/ion_slider_input.html',
                      'id': 'window_size',
                      'data_type': "single",
                      'data_grid': "false",
                      'data_min': self.min_value,
                      'data_max': self.max_value,
                      'data_from': self.initial,
                      'data_step': "1",
                      'help_text_in_popover': True}


class RandomSeedIntegerField(serializers.IntegerField):
    def __init__(self, **kwargs):
        super(RandomSeedIntegerField, self).__init__(**kwargs)
        self.label = 'Random Seed'
        self.help_text = 'The seed used by the random number generator when randomly selecting training and validation data. If you provide the same seed again in a later computation, you get the same selection of data.'
        self.style = {'template': 'vadetisweb/parts/input/text_input.html',
                      'placeholder': 'e.g. 42',
                      'help_text_in_popover': True}


class TimeRangeChoiceField(serializers.ChoiceField):
    def __init__(self, **kwargs):
        super(TimeRangeChoiceField, self).__init__(choices=TIME_RANGE, **kwargs)
        self.label = 'Time Range'
        self.help_text = 'The time range to apply anomaly detection'
        self.style = {'template': 'vadetisweb/parts/input/select_input.html',
                      'id': 'timeRange',
                      'help_text_in_popover': True}


class MaximizeScoreChoiceField(serializers.ChoiceField):
    def __init__(self, **kwargs):
        super(MaximizeScoreChoiceField, self).__init__(choices=ANOMALY_DETECTION_SCORE_TYPES, **kwargs)
        self.label = 'Maximize Score'
        self.help_text = 'Define which score you want to maximize for the results. In order to achive the best score out of this selection, the most appropiate threshold value will be selected. You can further change the threshold after computation.'
        self.style = {'template': 'vadetisweb/parts/input/select_input.html',
                      'help_text_in_popover': True}


class RangeStartHiddenIntegerField(serializers.IntegerField):
    def __init__(self, **kwargs):
        html_id = kwargs.pop('html_id', 'rangeStart')
        super(RangeStartHiddenIntegerField, self).__init__(**kwargs)
        self.required = True
        self.min_value = 0
        self.style = {'template': 'vadetisweb/parts/input/hidden_input.html',
                      'id': html_id }


class RangeEndHiddenIntegerField(serializers.IntegerField):
    def __init__(self, **kwargs):
        html_id = kwargs.pop('html_id', 'rangeEnd')
        super(RangeEndHiddenIntegerField, self).__init__(**kwargs)
        self.required = True
        self.min_value = 0
        self.style = {'template': 'vadetisweb/parts/input/hidden_input.html',
                      'id': html_id }
