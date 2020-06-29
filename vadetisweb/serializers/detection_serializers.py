from vadetisweb.models import *
from vadetisweb.fields import *


class AlgorithmSerializer(serializers.Serializer):
    empty_choice = ('', '----')
    ANOMALY_DETECTION_ALGORITHMS_EMPTY = (empty_choice,) + ANOMALY_DETECTION_ALGORITHMS

    algorithm = serializers.ChoiceField(choices=ANOMALY_DETECTION_ALGORITHMS_EMPTY,
                                        required=True,
                                        help_text='The type of anomaly detection algorithm',
                                        style={'template': 'vadetisweb/parts/input/select_input_onchange_submit.html',
                                               'help_text_in_popover': True})

    def __init__(self, *args, **kwargs):
        super(AlgorithmSerializer, self).__init__(*args, **kwargs)


class RPCAMEstimatorLossSerializer(serializers.Serializer):
    dataset = DatasetField(default='overridden')
    dataset_series_json = DatasetJsonField(initial=None, binary=False, encoder=None,
                                           style={'template': 'vadetisweb/parts/input/hidden_input.html',
                                                  'id': 'dataset_series_json'})

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

    training_dataset = TrainingDatasetField(label='Training Dataset',
                                            required=True,
                                            queryset=DataSet.objects.none())
    train_size = TrainSizeFloatField(initial=0.5, min_value=0.001, max_value=0.999, required=True)
    random_seed = RandomSeedIntegerField(initial=10, required=False)
    time_range = TimeRangeChoiceField(required=True)
    maximize_score = MaximizeScoreChoiceField(required=True)
    range_start = RangeStartHiddenIntegerField()
    range_end = RangeEndHiddenIntegerField()

    def __init__(self, *args, **kwargs):
        super(RPCAMEstimatorLossSerializer, self).__init__(*args, **kwargs)


class HistogramSerializer(serializers.Serializer):
    dataset = DatasetField(default='overridden')
    dataset_series_json = DatasetJsonField(initial=None, binary=False, encoder=None,
                                           style={'template': 'vadetisweb/parts/input/hidden_input.html',
                                                  'id': 'dataset_series_json'})

    training_dataset = TrainingDatasetField(label='Training Dataset',
                                            required=True,
                                            queryset=DataSet.objects.none())
    train_size = TrainSizeFloatField(initial=0.5, min_value=0.001, max_value=0.999, required=True)
    random_seed = RandomSeedIntegerField(initial=10, required=False)
    time_range = TimeRangeChoiceField(required=True)
    maximize_score = MaximizeScoreChoiceField(required=True)
    range_start = RangeStartHiddenIntegerField()
    range_end = RangeEndHiddenIntegerField()

    def __init__(self, *args, **kwargs):
        super(HistogramSerializer, self).__init__(*args, **kwargs)

class ClusterSerializer(serializers.Serializer):
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

    train_size = TrainSizeFloatField(initial=0.5, min_value=0.001, max_value=0.999, required=True)
    random_seed = RandomSeedIntegerField(initial=10, required=False)
    time_range = TimeRangeChoiceField(required=True)
    maximize_score = MaximizeScoreChoiceField(required=True)
    range_start = RangeStartHiddenIntegerField()
    range_end = RangeEndHiddenIntegerField()

    def __init__(self, *args, **kwargs):
        super(ClusterSerializer, self).__init__(*args, **kwargs)


class SVMSerializer(serializers.Serializer):
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
    train_size = TrainSizeFloatField(initial=0.5, min_value=0.001, max_value=0.999, required=True)

    random_seed = RandomSeedIntegerField(initial=10, required=False)
    time_range = TimeRangeChoiceField(required=True)
    maximize_score = MaximizeScoreChoiceField(required=True)
    range_start = RangeStartHiddenIntegerField()
    range_end = RangeEndHiddenIntegerField()

    def __init__(self, *args, **kwargs):
        super(SVMSerializer, self).__init__(*args, **kwargs)


class IsolationForestSerializer(serializers.Serializer):
    dataset = DatasetField(default='overridden')
    dataset_series_json = DatasetJsonField(initial=None, binary=False, encoder=None,
                                           style={'template': 'vadetisweb/parts/input/hidden_input.html',
                                                  'id': 'dataset_series_json'})

    training_dataset = TrainingDatasetField(label='Training Dataset',
                                            required=True,
                                            queryset=DataSet.objects.none())
    bootstrap = serializers.BooleanField(label='Bootstrap', required=False,
                                         help_text='If True, individual trees are fit on random subsets of the training data sampled with replacement. If False, sampling without replacement is performed.',
                                         style={'help_text_in_popover': True})
    n_estimators = serializers.IntegerField(initial=40, label='Number of Estimators', min_value=1, required=True,
                                            help_text='The number of base estimators in the ensemble.',
                                            style={'template': 'vadetisweb/parts/input/text_input.html',
                                                   'help_text_in_popover': True})
    train_size = TrainSizeFloatField(initial=0.5, min_value=0.001, max_value=0.999, required=True)

    random_seed = RandomSeedIntegerField(initial=10, required=False)
    time_range = TimeRangeChoiceField(required=True)
    maximize_score = MaximizeScoreChoiceField(required=True)
    range_start = RangeStartHiddenIntegerField()
    range_end = RangeEndHiddenIntegerField()

    def __init__(self, *args, **kwargs):
        super(IsolationForestSerializer, self).__init__(*args, **kwargs)


class LisaPearsonSerializer(serializers.Serializer):
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
                                  many=True,
                                  allow_empty=False,
                                  allow_null=False,
                                  style={'template': 'vadetisweb/parts/input/checkbox_multiple_input.html',
                                         'inline': True,
                                         'help_text_in_popover': True})

    window_size = serializers.IntegerField(initial=12, required=True, min_value=1,
                                           help_text='Select the moving window size as a percentage value relative to the length of the time series or as an absolute value range.',
                                           style={'template': 'vadetisweb/parts/input/text_input.html',
                                                  'help_text_in_popover': True})
    window_size_unit = serializers.ChoiceField(choices=WINDOW_SIZES, required=True,
                                               style={'template': 'vadetisweb/parts/input/select_input.html',
                                                      'help_text_in_popover': True})
    row_standardized = serializers.BooleanField(initial=True, label='Apply Row Standardization', required=False,
                                                help_text='Determines if row standardization is applied to the correlation values',
                                                style={'help_text_in_popover': True})

    anomaly_type = serializers.ChoiceField(choices=ANOMALY_TYPES, required=True,
                                           help_text='Marks anomalies either individually for each time series or together as anomalous instances.',
                                           style={'template': 'vadetisweb/parts/input/select_input.html',
                                                  'help_text_in_popover': True})

    time_range = TimeRangeChoiceField(required=True)
    maximize_score = MaximizeScoreChoiceField(required=True)
    range_start = RangeStartHiddenIntegerField()
    range_end = RangeEndHiddenIntegerField()


class LisaDtwPearsonSerializer(serializers.Serializer):
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
                                  many=True,
                                  allow_empty=False,
                                  allow_null=False,
                                  style={'template': 'vadetisweb/parts/input/checkbox_multiple_input.html',
                                         'inline': True,
                                         'help_text_in_popover': True})

    window_size = serializers.IntegerField(initial=12, required=True, min_value=1,
                                           help_text='Select the moving window size as a percentage value relative to the length of the time series or as an absolute value range.',
                                           style={'template': 'vadetisweb/parts/input/text_input.html',
                                                  'help_text_in_popover': True})
    window_size_unit = serializers.ChoiceField(choices=WINDOW_SIZES, required=True,
                                               style={'template': 'vadetisweb/parts/input/select_input.html',
                                                      'help_text_in_popover': True})
    dtw_distance_function = serializers.ChoiceField(label='DTW Distance Function', choices=DTW_DISTANCE_FUNCTION,
                                                    required=True,
                                                    help_text='The distance function used to calculate the cost between values.',
                                                    style={'template': 'vadetisweb/parts/input/select_input.html',
                                                           'help_text_in_popover': True})
    row_standardized = serializers.BooleanField(initial=True, label='Apply Row Standardization', required=False,
                                                help_text='Determines if row standardization is applied to the correlation values',
                                                style={'help_text_in_popover': True})

    anomaly_type = serializers.ChoiceField(choices=ANOMALY_TYPES, required=True,
                                           help_text='Marks anomalies either individually for each time series or together as anomalous instances.',
                                           style={'template': 'vadetisweb/parts/input/select_input.html',
                                                  'help_text_in_popover': True})

    time_range = TimeRangeChoiceField(required=True)
    maximize_score = MaximizeScoreChoiceField(required=True)
    range_start = RangeStartHiddenIntegerField()
    range_end = RangeEndHiddenIntegerField()


class LisaGeoDistanceSerializer(serializers.Serializer):
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
                                  many=True,
                                  allow_empty=False,
                                  allow_null=False,
                                  style={'template': 'vadetisweb/parts/input/checkbox_multiple_input.html',
                                         'inline': True,
                                         'help_text_in_popover': True})

    geo_distance_function = serializers.ChoiceField(choices=GEO_DISTANCE, required=True,
                                                    help_text='The geographic distance function used for the calculation.',
                                                    style={'template': 'vadetisweb/parts/input/select_input.html',
                                                           'help_text_in_popover': True})

    anomaly_type = serializers.ChoiceField(choices=ANOMALY_TYPES, required=True,
                                           help_text='Marks anomalies either individually for each time series or together as anomalous instances.',
                                           style={'template': 'vadetisweb/parts/input/select_input.html',
                                                  'help_text_in_popover': True})

    time_range = serializers.ChoiceField(label='Time Range', choices=TIME_RANGE, required=True,
                                         help_text='The time range to apply anomaly detection',
                                         style={'template': 'vadetisweb/parts/input/select_input.html',
                                                'help_text_in_popover': True})
    maximize_score = serializers.ChoiceField(label='Maximize Score', choices=ANOMALY_DETECTION_SCORE_TYPES,
                                             required=True,
                                             help_text='Define which score you want to maximize for the results. In order to achive the best score out of this selection, the most appropiate threshold value will be selected. You can further change the threshold after computation.',
                                             style={'template': 'vadetisweb/parts/input/select_input.html',
                                                    'help_text_in_popover': True})
    range_start = RangeStartHiddenIntegerField()
    range_end = RangeEndHiddenIntegerField()

    def __init__(self, *args, **kwargs):
        # post_data = args[0]
        super(LisaGeoDistanceSerializer, self).__init__(*args, **kwargs)
        """time_series = TimeSeries.objects.filter(datasets__in=[post_data['dataset_selected']])

        all_have_ch1903 = True
        all_have_height = True
        for ts in time_series:
            if ts.location.ch1903_easting == None or ts.location.ch1903_northing == None:
                all_have_ch1903 = False
            if ts.location.height == None:
                all_have_height = False

        if not all_have_ch1903:
            self.fields['geo_distance_function'].choices = ((HAVERSINE, HAVERSINE),)
        elif not all_have_height:
            self.fields['geo_distance_function'].choices = ((CH1903, CH1903), (HAVERSINE, HAVERSINE),)"""


class ThresholdSerializer(serializers.Serializer):
    dataset_series_json = DatasetJsonField(initial=None, binary=False, encoder=None,
                                           style={'template': 'vadetisweb/parts/input/hidden_input.html',
                                                  'id': 'dataset_series_json'})

    threshold = serializers.FloatField(label='New Threshold', required=True,
                                       style={'template': 'vadetisweb/parts/input/text_input_slider.html',
                                              'step': 'any',
                                              'id': 'threshold_value',
                                              'help_text_in_popover': True},
                                       help_text='You can set a new threshold from most suitable value range with the slider or through text input. '
                                                 'If you manually set a value out of range, the slider will adapt to the new range.')

    def __init__(self, *args, **kwargs):
        super(ThresholdSerializer, self).__init__(*args, **kwargs)
