from vadetisweb.models import *
from vadetisweb.fields import *
from vadetisweb.utils.anomaly_detection_utils import get_detection_choices

class ConditionalRequiredFieldMixin:
    """
    Allows to use serializer methods to allow change field is required or not
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            method_name = f'is_{field_name}_required'
            if hasattr(self, method_name):
                field.required = getattr(self, method_name)()


class AlgorithmSerializer(serializers.Serializer):
    empty_choice = ('', '----')
    # choices are loaded from context
    algorithm = serializers.ChoiceField(choices=empty_choice, required=True,
                                        help_text='Select the algorithm you want to use for detection. The possibilities depend on whether training data and spatial data are avaiable or not.',
                                        style={'template': 'vadetisweb/parts/input/select_input.html',
                                               'id': 'detectionOnChange',
                                               'help_text_in_popover': True})

    def __init__(self, *args, **kwargs):
        super(AlgorithmSerializer, self).__init__(*args, **kwargs)
        dataset = self.context.get('dataset', None)
        self.fields['algorithm'].choices = get_detection_choices(dataset)


class RPCAMEstimatorLossSerializer(ConditionalRequiredFieldMixin, serializers.Serializer):
    dataset = DatasetField(default='overridden')
    dataset_series_json = DatasetJsonField(initial=None, binary=False, encoder=None,
                                           style={'template': 'vadetisweb/parts/input/hidden_input.html',
                                                  'id': 'dataset_series_json'})

    training_dataset = TrainingDatasetField(label='Training Dataset',
                                            required=True,
                                            queryset=DataSet.objects.none())

    delta = serializers.FloatField(initial=1.0, label='Delta', required=True,
                                   help_text='Delta for Huber Loss function. The value of delta depends on the contamination level of the data. '
                                             'The higher the contamination, the lower the value should be chosen.',
                                   style={'template': 'vadetisweb/parts/input/text_input.html',
                                          'step': 'any',
                                          'help_text_in_popover': True})

    n_components = serializers.IntegerField(initial=2, label='Number of components', min_value=2, required=True,
                                            help_text='The number of components for dimensionality reduction.',
                                            style={'template': 'vadetisweb/parts/input/text_input.html',
                                                   'step': 'any', 'min': 2,
                                                   'help_text_in_popover': True})

    train_size = TrainSizeFloatField(initial=0.5, min_value=0.2, max_value=0.8, required=True)

    time_range = TimeRangeChoiceField(required=True)
    maximize_score = MaximizeScoreChoiceField(required=True)
    range_start = RangeStartHiddenIntegerField()
    range_end = RangeEndHiddenIntegerField()

    def is_dataset_series_json_required(self):
        required = self.context.get('dataset_series_json_required', True)
        if not required:
            return False
        return True

    def __init__(self, *args, **kwargs):
        super(RPCAMEstimatorLossSerializer, self).__init__(*args, **kwargs)


class HistogramSerializer(ConditionalRequiredFieldMixin, serializers.Serializer):
    dataset = DatasetField(default='overridden')
    dataset_series_json = DatasetJsonField(initial=None, binary=False, encoder=None,
                                           style={'template': 'vadetisweb/parts/input/hidden_input.html',
                                                  'id': 'dataset_series_json'})

    training_dataset = TrainingDatasetField(label='Training Dataset',
                                            required=True,
                                            queryset=DataSet.objects.none())
    train_size = TrainSizeFloatField(initial=0.5, min_value=0.2, max_value=0.8, required=True)
    time_range = TimeRangeChoiceField(required=True)
    maximize_score = MaximizeScoreChoiceField(required=True)
    range_start = RangeStartHiddenIntegerField()
    range_end = RangeEndHiddenIntegerField()

    def is_dataset_series_json_required(self):
        required = self.context.get('dataset_series_json_required', True)
        if not required:
            return False
        return True

    def __init__(self, *args, **kwargs):
        super(HistogramSerializer, self).__init__(*args, **kwargs)


class ClusterSerializer(ConditionalRequiredFieldMixin, serializers.Serializer):
    dataset = DatasetField(default='overridden')
    dataset_series_json = DatasetJsonField(initial=None, binary=False, encoder=None,
                                           style={'template': 'vadetisweb/parts/input/hidden_input.html',
                                                  'id': 'dataset_series_json'})

    training_dataset = TrainingDatasetField(label='Training Dataset',
                                            required=True,
                                            queryset=DataSet.objects.none())
    n_components = serializers.IntegerField(initial=3, label='Number of Components', min_value=1, required=True,
                                            help_text='The number of mixture components.',
                                            style={'template': 'vadetisweb/parts/input/text_input.html',
                                                   'step': 'any',
                                                   'min': 1,
                                                   'help_text_in_popover': True})
    n_init = serializers.IntegerField(initial=3, label='Number of Inits', min_value=1, required=True,
                                      help_text='The number of initializations to perform. The best results are kept.',
                                      style={'template': 'vadetisweb/parts/input/text_input.html',
                                             'help_text_in_popover': True})

    train_size = TrainSizeFloatField(initial=0.5, min_value=0.2, max_value=0.8, required=True)
    time_range = TimeRangeChoiceField(required=True)
    maximize_score = MaximizeScoreChoiceField(required=True)
    range_start = RangeStartHiddenIntegerField()
    range_end = RangeEndHiddenIntegerField()

    def is_dataset_series_json_required(self):
        required = self.context.get('dataset_series_json_required', True)
        if not required:
            return False
        return True

    def __init__(self, *args, **kwargs):
        super(ClusterSerializer, self).__init__(*args, **kwargs)


class SVMSerializer(ConditionalRequiredFieldMixin, serializers.Serializer):
    dataset = DatasetField(default='overridden')
    dataset_series_json = DatasetJsonField(initial=None, binary=False, encoder=None,
                                           style={'template': 'vadetisweb/parts/input/hidden_input.html',
                                                  'id': 'dataset_series_json'})

    training_dataset = TrainingDatasetField(label='Training Dataset',
                                            required=True,
                                            queryset=DataSet.objects.none())
    kernel = serializers.ChoiceField(label='Kernel', choices=SVM_KERNELS, required=True,
                                     help_text='The kernel for the SVM.',
                                     style={'template': 'vadetisweb/parts/input/select_input.html',
                                            'help_text_in_popover': True})
    gamma = serializers.FloatField(initial=0.0005, label='Gamma', min_value=0.00000001, max_value=1, required=False,
                                   help_text='Kernel coefficient for \'rbf\', \'poly\' and \'sigmoid\'; ignored for \'linear\' kernel. The optimal value depends entirely on the data. If gamma is \'None\' then (1 / Number of features) will be used instead.',
                                   style={'template': 'vadetisweb/parts/input/text_input.html',
                                          'step': 'any',
                                          'min': 0.000001,
                                          'max': 1,
                                          'help_text_in_popover': True})
    nu = serializers.FloatField(initial=0.95, label='Nu', min_value=0.000001, max_value=1, required=False,
                                help_text='An upper bound on the fraction of training errors and a lower bound of the fraction of support vectors. Should be in the interval (0, 1]. If none, the default value 0.5 will be used.',
                                style={'template': 'vadetisweb/parts/input/text_input.html',
                                       'step': 'any',
                                       'min': 0.000001,
                                       'max': 1,
                                       'help_text_in_popover': True})
    train_size = TrainSizeFloatField(initial=0.5, min_value=0.2, max_value=0.8, required=True)

    time_range = TimeRangeChoiceField(required=True)
    maximize_score = MaximizeScoreChoiceField(required=True)
    range_start = RangeStartHiddenIntegerField()
    range_end = RangeEndHiddenIntegerField()

    def is_dataset_series_json_required(self):
        required = self.context.get('dataset_series_json_required', True)
        if not required:
            return False
        return True

    def __init__(self, *args, **kwargs):
        super(SVMSerializer, self).__init__(*args, **kwargs)


class IsolationForestSerializer(ConditionalRequiredFieldMixin, serializers.Serializer):
    dataset = DatasetField(default='overridden')
    dataset_series_json = DatasetJsonField(initial=None, binary=False, encoder=None,
                                           style={'template': 'vadetisweb/parts/input/hidden_input.html',
                                                  'id': 'dataset_series_json'})

    training_dataset = TrainingDatasetField(label='Training Dataset',
                                            required=True,
                                            queryset=DataSet.objects.none())

    bootstrap = serializers.BooleanField(label='Bootstrap', required=False,
                                         help_text='If True, individual trees are fit on random subsets of the training data sampled with replacement. If False, sampling without replacement is performed.',
                                         style={'help_text_in_popover': False,
                                                'template': 'vadetisweb/parts/input/checkbox_input.html'})

    n_estimators = serializers.IntegerField(initial=40, label='Number of Estimators', min_value=1, required=True,
                                            help_text='The number of base estimators in the ensemble.',
                                            style={'template': 'vadetisweb/parts/input/text_input.html',
                                                   'help_text_in_popover': True})
    train_size = TrainSizeFloatField(initial=0.5, min_value=0.2, max_value=0.8, required=True)

    time_range = TimeRangeChoiceField(required=True)
    maximize_score = MaximizeScoreChoiceField(required=True)
    range_start = RangeStartHiddenIntegerField()
    range_end = RangeEndHiddenIntegerField()

    def is_dataset_series_json_required(self):
        required = self.context.get('dataset_series_json_required', True)
        if not required:
            return False
        return True

    def __init__(self, *args, **kwargs):
        super(IsolationForestSerializer, self).__init__(*args, **kwargs)


class LisaPearsonSerializer(ConditionalRequiredFieldMixin, serializers.Serializer):
    """
    The serializer for the parameters for Pearson correlation algorithm
    """

    dataset = DatasetField(default='overridden')
    dataset_series_json = DatasetJsonField(initial=None, binary=False, encoder=None,
                                           style={'template': 'vadetisweb/parts/input/hidden_input.html',
                                                  'id': 'dataset_series_json'})

    time_series = TimeSeriesField(label='Time Series',
                                  queryset=TimeSeries.objects.none(),
                                  required=True,
                                  many=False,
                                  allow_empty=False,
                                  allow_null=False,
                                  style={'template': 'vadetisweb/parts/input/select_input.html',
                                         'help_text_in_popover': True})

    window_size = WindowSizeIntegerField(initial=10, required=True, min_value=2, max_value=20)

    time_range = TimeRangeChoiceField(required=True)
    maximize_score = MaximizeScoreChoiceField(required=True)
    range_start = RangeStartHiddenIntegerField()
    range_end = RangeEndHiddenIntegerField()

    def is_dataset_series_json_required(self):
        required = self.context.get('dataset_series_json_required', True)
        if not required:
            return False
        return True

    def __init__(self, *args, **kwargs):
        super(LisaPearsonSerializer, self).__init__(*args, **kwargs)


class LisaDtwPearsonSerializer(ConditionalRequiredFieldMixin, serializers.Serializer):
    """
    The serializer for the parameters for DTW with Pearson correlation algorithm
    """
    dataset = DatasetField(default='overridden')
    dataset_series_json = DatasetJsonField(initial=None, binary=False, encoder=None,
                                           style={'template': 'vadetisweb/parts/input/hidden_input.html',
                                                  'id': 'dataset_series_json'})

    time_series = TimeSeriesField(label='Time Series',
                                  queryset=TimeSeries.objects.none(),
                                  required=True,
                                  many=False,
                                  allow_empty=False,
                                  allow_null=False,
                                  style={'template': 'vadetisweb/parts/input/select_input.html',
                                         'help_text_in_popover': True})

    window_size = WindowSizeIntegerField(initial=10, required=True, min_value=2, max_value=20)

    dtw_distance_function = serializers.ChoiceField(label='DTW Distance Function', choices=DTW_DISTANCE_FUNCTION,
                                                    required=True,
                                                    help_text='The distance function used to calculate the cost between values.',
                                                    style={'template': 'vadetisweb/parts/input/select_input.html',
                                                           'help_text_in_popover': True})

    time_range = TimeRangeChoiceField(required=True)
    maximize_score = MaximizeScoreChoiceField(required=True)
    range_start = RangeStartHiddenIntegerField()
    range_end = RangeEndHiddenIntegerField()

    def is_dataset_series_json_required(self):
        required = self.context.get('dataset_series_json_required', True)
        if not required:
            return False
        return True

    def __init__(self, *args, **kwargs):
        super(LisaDtwPearsonSerializer, self).__init__(*args, **kwargs)


class LisaGeoDistanceSerializer(ConditionalRequiredFieldMixin, serializers.Serializer):
    """
    The serializer for the parameters for geographical correlation algorithm
    """
    dataset = DatasetField(default='overridden')
    dataset_series_json = DatasetJsonField(initial=None, binary=False, encoder=None,
                                           style={'template': 'vadetisweb/parts/input/hidden_input.html',
                                                  'id': 'dataset_series_json'})

    time_series = TimeSeriesField(label='Time Series',
                                  queryset=TimeSeries.objects.none(),
                                  required=True,
                                  many=False,
                                  allow_empty=False,
                                  allow_null=False,
                                  style={'template': 'vadetisweb/parts/input/select_input.html',
                                         'help_text_in_popover': True})

    time_range = TimeRangeChoiceField(required=True)

    maximize_score = serializers.ChoiceField(label='Maximize Score', choices=ANOMALY_DETECTION_SCORE_TYPES,
                                             required=True,
                                             help_text='Define which score you want to maximize for the results. In order to achive the best score out of this selection, the most appropiate threshold value will be selected. You can further change the threshold after computation.',
                                             style={'template': 'vadetisweb/parts/input/select_input.html',
                                                    'help_text_in_popover': True})

    range_start = RangeStartHiddenIntegerField()
    range_end = RangeEndHiddenIntegerField()

    def is_dataset_series_json_required(self):
        required = self.context.get('dataset_series_json_required', True)
        if not required:
            return False
        return True

    def __init__(self, *args, **kwargs):
        # post_data = args[0]
        super(LisaGeoDistanceSerializer, self).__init__(*args, **kwargs)


class ThresholdSerializer(serializers.Serializer):
    dataset_series_json = DatasetJsonField(initial=None, binary=False, encoder=None,
                                           style={'template': 'vadetisweb/parts/input/hidden_input.html',
                                                  'id': 'dataset_series_json'})

    threshold = serializers.FloatField(label='New Threshold', required=True,
                                       help_text='You can set a new threshold from most suitable value range with the slider or through text input. '
                                                 'If you manually set a value out of range, the slider will adapt to the new range.',
                                       style={'template': 'vadetisweb/parts/input/text_input_slider.html',
                                              'step': 'any',
                                              'id': 'threshold_value',
                                              'help_text_in_popover': False})

    upper_boundary = serializers.BooleanField(default=False, initial=False,
                                              style={'template': 'vadetisweb/parts/input/hidden_input.html',
                                                     'id': 'upper_boundary'})

    def __init__(self, *args, **kwargs):
        super(ThresholdSerializer, self).__init__(*args, **kwargs)
