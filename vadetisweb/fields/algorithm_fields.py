from rest_framework import serializers
from vadetisweb.parameters import TIME_RANGE, ANOMALY_DETECTION_SCORE_TYPES
from vadetisweb.models import DataSet, TimeSeries


class TrainingDatasetField(serializers.PrimaryKeyRelatedField):
    def get_queryset(self):
        dataset_selected = self.context.get('dataset_selected', None)
        if dataset_selected is not None:
            return DataSet.objects.filter(original_dataset__id=dataset_selected, is_training_data=True)
        return DataSet.objects.none()

    def display_value(self, instance):
        return instance.title


class TimeSeriesField(serializers.PrimaryKeyRelatedField):

    def __init__(self, **kwargs):
        super(TimeSeriesField, self).__init__(**kwargs)
        self.style = {'template': 'vadetisweb/parts/input/select_input_onchange_submit.html'}


    def get_queryset(self):
        dataset_selected = self.context.get('dataset_selected', None)
        #timeseries_selected = self.context.get('timeseries_selected', None)
        if dataset_selected is not None:
            return TimeSeries.objects.filter(datasets__in=[dataset_selected])
        return TimeSeries.objects.none()

    def display_value(self, instance):
        return instance.name


class TrainSizeFloatField(serializers.FloatField):
    def __init__(self, **kwargs):
        super(TrainSizeFloatField, self).__init__(**kwargs)
        self.label = 'Train Size'
        self.help_text = 'Represent the proportion of the training dataset to use for model training. The rest of the data will be used to validate the model. Should be in the interval (0, 1).'
        self.style = {'template': 'vadetisweb/parts/input/text_input.html', 'placeholder': 'e.g. 0.5', 'step': 'any', 'min': self.min_value, 'max': self.max_value }


class RandomSeedIntegerField(serializers.IntegerField):
    def __init__(self, **kwargs):
        super(RandomSeedIntegerField, self).__init__(**kwargs)
        self.label = 'Random Seed'
        self.help_text = 'The seed used by the random number generator when randomly selecting training and validation data. If you provide the same seed again in a later computation, you get the same selection of data.'
        self.style = {'template': 'vadetisweb/parts/input/text_input.html', 'placeholder': 'e.g. 42'}


class TimeRangeChoiceField(serializers.ChoiceField):
    def __init__(self, **kwargs):
        super(TimeRangeChoiceField, self).__init__(choices=TIME_RANGE, **kwargs)
        self.label = 'Time Range'
        self.help_text = 'The time range to apply anomaly detection'
        self.style = {'template': 'vadetisweb/parts/input/select_input.html', 'id': 'id_time_range' }


class MaximizeScoreChoiceField(serializers.ChoiceField):
    def __init__(self, **kwargs):
        super(MaximizeScoreChoiceField, self).__init__(choices=ANOMALY_DETECTION_SCORE_TYPES,**kwargs)
        self.label = 'Maximize Score'
        self.help_text = 'Define which score you want to maximize for the results. In order to achive the best score out of this selection, the most appropiate threshold value will be selected. You can further change the threshold after computation.'
        self.style = {'template': 'vadetisweb/parts/input/select_input.html'}

