from rest_framework import serializers
from vadetisweb.parameters import *
from vadetisweb.models import *
from vadetisweb.fields import *
from vadetisweb.parameters import HISTOGRAM, FULL
from django.utils import timezone

"""
class AlgorithmAnomalyDetection(object):

    def get_algorithm(self):
        return self.algorithm

    def __init__(self, dataset_selected, algorithm, *args, **kwargs):
        self.dataset_selected = int(dataset_selected)
        self.algorithm = algorithm


class HistogramAnomalyDetection(AlgorithmAnomalyDetection):

    def __init__(self, *args, **kwargs):
        super(AlgorithmAnomalyDetection, self).__init__(*args, **kwargs)
        self.train_size = kwargs.pop('train_size', None)
        self.random_seed = kwargs.pop('random_seed', None)
        self.time_range = kwargs.pop('time_range', FULL)
        self.maximize_score = kwargs.pop('maximize_score', F1_SCORE)
        self.range_start = kwargs.pop('range_start', 0)
        self.range_end = kwargs.pop('range_end', 0)
        
        
class ClusterAnomalyDetection(AlgorithmAnomalyDetection):
    
    def __init__(self, *args, **kwargs):
        super(AlgorithmAnomalyDetection, self).__init__(*args, **kwargs)
        self.td_selected = kwargs.pop('td_selected', None)
        self.n_components = kwargs.pop('n_components', None)
        self.n_init = kwargs.pop('n_init', None)
        self.train_size = kwargs.pop('train_size', None)
        self.random_seed = kwargs.pop('random_seed', None)
        self.time_range = kwargs.pop('time_range', FULL)
        self.maximize_score = kwargs.pop('maximize_score', F1_SCORE)
        self.range_start = kwargs.pop('range_start', 0)
        self.range_end = kwargs.pop('range_end', 0)
"""

class AlgorithmSerializer(serializers.Serializer):
    empty_choice = ('', '----')
    ANOMALY_DETECTION_ALGORITHMS_EMPTY = (empty_choice,) + ANOMALY_DETECTION_ALGORITHMS

    modified = serializers.ReadOnlyField(default=timezone.now)
    dataset_selected = serializers.HiddenField(default=None)
    algorithm = serializers.ChoiceField(choices=ANOMALY_DETECTION_ALGORITHMS_EMPTY,
                                        required=True,
                                        source='get_algorithm',
                                        help_text='The type of anomaly detection algorithm')

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        loaded_dataset = kwargs.pop('dataset', None)
        super(AlgorithmSerializer, self).__init__(*args, **kwargs)
        self.fields['modified'].initial = "ABC"


class HistogramSerializer(AlgorithmSerializer):
    td_selected = TrainingDatasetField(label='Training Dataset',
                                       required=True,
                                       queryset=DataSet.objects.none())
    train_size = TrainSizeFloatField(min_value=0.001, max_value=0.999, required=True)
    random_seed = RandomSeedIntegerField(required=False)
    time_range = TimeRangeChoiceField(required=True)
    maximize_score = MaximizeScoreChoiceField(required=True)
    range_start = serializers.IntegerField(required=True, min_value=0,
                                           style={'template': 'vadetisweb/parts/input/hidden_input.html'})
    range_end = serializers.IntegerField(required=True, min_value=0,
                                         style={'template': 'vadetisweb/parts/input/hidden_input.html'})

    def __init__(self, *args, **kwargs):
        super(HistogramSerializer, self).__init__(*args, **kwargs)


class ClusterSerializer(AlgorithmSerializer):
    td_selected = TrainingDatasetField(label='Training Dataset',
                                       required=True,
                                       queryset=DataSet.objects.none())
    n_components = serializers.IntegerField(label='Number of Components', min_value=1, required=True,
                                            help_text='The number of mixture components.',
                                            style={'template': 'vadetisweb/parts/input/text_input.html'})
    n_init = serializers.IntegerField(label='Number of Inits', min_value=1, required=True,
                                      help_text='The number of initializations to perform. The best results are kept.',
                                      style={'template': 'vadetisweb/parts/input/text_input.html'})
    train_size = TrainSizeFloatField(min_value=0.001, max_value=0.999, required=True)
    random_seed = RandomSeedIntegerField(required=False)
    time_range = TimeRangeChoiceField(required=True)
    maximize_score = MaximizeScoreChoiceField(required=True)
    range_start = serializers.IntegerField(required=True, min_value=0,
                                           style={'template': 'vadetisweb/parts/input/hidden_input.html'})
    range_end = serializers.IntegerField(required=True, min_value=0,
                                         style={'template': 'vadetisweb/parts/input/hidden_input.html'})

    def __init__(self, *args, **kwargs):
        super(ClusterSerializer, self).__init__(*args, **kwargs)


class SVMSerializer(AlgorithmSerializer):
    td_selected = TrainingDatasetField(label='Training Dataset',
                                       required=True,
                                       queryset=DataSet.objects.none())
    kernel = serializers.ChoiceField(label='Kernel', choices=SVM_KERNELS, required=True,
                                     help_text='The kernel for the SVM.',
                                     style={'template': 'vadetisweb/parts/input/select_input.html'})
    gamma = serializers.FloatField(label='Gamma', min_value=0.00000001, max_value=1, required=False,
                                   help_text='Kernel coefficient for \'rbf\', \'poly\' and \'sigmoid\'; ignored for \'linear\' kernel. The optimal value depends entirely on the data. If gamma is \'None\' then (1 / Number of features) will be used instead.',
                                   style={'template': 'vadetisweb/parts/input/text_input.html'})
    nu = serializers.FloatField(label='Nu', min_value=0.000001, max_value=1, required=False,
                                help_text='An upper bound on the fraction of training errors and a lower bound of the fraction of support vectors. Should be in the interval (0, 1]. If none, the default value 0.5 will be used.',
                                style={'template': 'vadetisweb/parts/input/text_input.html'})
    train_size = TrainSizeFloatField(min_value=0.001, max_value=0.999, required=True)
    random_seed = RandomSeedIntegerField(required=False)
    time_range = TimeRangeChoiceField(required=True)
    maximize_score = MaximizeScoreChoiceField(required=True)
    range_start = serializers.IntegerField(required=True, min_value=0,
                                           style={'template': 'vadetisweb/parts/input/hidden_input.html'})
    range_end = serializers.IntegerField(required=True, min_value=0,
                                         style={'template': 'vadetisweb/parts/input/hidden_input.html'})

    def __init__(self, *args, **kwargs):
        super(SVMSerializer, self).__init__(*args, **kwargs)


class IsolationForestSerializer(AlgorithmSerializer):

    td_selected = TrainingDatasetField(label='Training Dataset',
                                       required=True,
                                       queryset=DataSet.objects.none())
    bootstrap = serializers.BooleanField(label='Bootstrap', required=False,
                                         help_text='If True, individual trees are fit on random subsets of the training data sampled with replacement. If False, sampling without replacement is performed.',
                                         style={'template': 'vadetisweb/parts/input/select_input.html'})
    n_estimators = serializers.IntegerField(label='Number of Estimators', min_value=1, required=True,
                                            help_text='The number of base estimators in the ensemble.',
                                            style={'template': 'vadetisweb/parts/input/text_input.html'})
    train_size = TrainSizeFloatField(min_value=0.001, max_value=0.999, required=True)
    random_seed = RandomSeedIntegerField(required=False)
    time_range = TimeRangeChoiceField(required=True)
    maximize_score = MaximizeScoreChoiceField(required=True)
    range_start = serializers.IntegerField(required=True, min_value=0,
                                           style={'template': 'vadetisweb/parts/input/hidden_input.html'})
    range_end = serializers.IntegerField(required=True, min_value=0,
                                         style={'template': 'vadetisweb/parts/input/hidden_input.html'})

    def __init__(self, *args, **kwargs):
        super(IsolationForestSerializer, self).__init__(*args, **kwargs)


class TSSerializer(AlgorithmSerializer):
    """
    Time series anomaly detection form
    """
    ts_selected = TimeSeriesField(label='Perform anomaly detection for single time series',
                                  queryset=TimeSeries.objects.none())

    def __init__(self, *args, **kwargs):
        #post_data = args[0]
        super(TSSerializer, self).__init__(*args, **kwargs)
        #time_series = TimeSeries.objects.filter(datasets__in=[post_data['dataset_selected']])
        #self.fields['ts_selected'].queryset = time_series

    def validate_ts_selected(self):
        data = self.validated_data.get('ts_selected', None)
        if not data:
            raise serializers.ValidationError('This field is required.')
        else:
            data = data.id
        return data


class CorrelationSerializer(TSSerializer):
    """
    The serializer for selection of a correlation algorithm
    """

    empty_choice = ('', '----')
    CORRELATION_ALGORITHMS_EMPTY = (empty_choice,) + CORRELATION_ALGORITHMS
    correlation_algorithm = serializers.ChoiceField(label='Correlation Algorithm', choices=CORRELATION_ALGORITHMS_EMPTY,
                                                    required=True,
                                                    help_text='Algorithm used to calculate the correlation',
                                                    style={'template': 'vadetisweb/parts/input/select_input.html'})

    def __init__(self, *args, **kwargs):
        #post_data = args[0]
        super(CorrelationSerializer, self).__init__(*args, **kwargs)

        #dataset = DataSet.objects.get(id=post_data['dataset_selected'])
        #if not dataset.spatial_data == SPATIAL:
        #    empty_choice = ('', '----')
        #    CORRELATION_ALGORITHMS_NON_SPATIAL_EMPTY = (empty_choice,) + CORRELATION_ALGORITHMS_NON_SPATIAL
        #    self.fields['correlation_algorithm'].choices = CORRELATION_ALGORITHMS_NON_SPATIAL_EMPTY


class WindowSizeSerializer(serializers.Serializer):
    """
    Helper Serializer for window size that combines 2 fields
    """
    window_size_value = serializers.IntegerField(min_value=1,
                                                 style={'template': 'vadetisweb/parts/input/text_input.html'})
    window_size_unit = serializers.ChoiceField(choices=WINDOW_SIZES, required=True,
                                               style={'template': 'vadetisweb/parts/input/select_input.html'})


class PearsonSerializer(CorrelationSerializer):
    """
    The serializer for the parameters for Pearson correlation algorithm
    """

    window_size = WindowSizeSerializer(label='Window Size',
                                       help_text='Select the moving window size as a percentage value relative to the length of the time series or as an absolute value range.')
    row_standardized = serializers.BooleanField(initial=True, label='Apply Row Standardization', required=False,
                                                help_text='Determines if row standardization is applied to the correlation values',
                                                style={'template': 'vadetisweb/parts/input/text_input.html'})
    time_range = TimeRangeChoiceField(required=True)
    maximize_score = MaximizeScoreChoiceField(required=True)
    range_start = serializers.IntegerField(required=True, min_value=0,
                                           style={'template': 'vadetisweb/parts/input/hidden_input.html'})
    range_end = serializers.IntegerField(required=True, min_value=0,
                                         style={'template': 'vadetisweb/parts/input/hidden_input.html'})


class DTWPearsonSerializer(CorrelationSerializer):
    """
    The serializer for the parameters for DTW with Pearson correlation algorithm
    """

    window_size = WindowSizeSerializer(label='Window Size',
                                       help_text='Select the moving window size as a percentage value relative to the length of the time series or as an absolute value range.')
    dtw_distance_function = serializers.ChoiceField(label='DTW Distance Function', choices=DTW_DISTANCE_FUNCTION,
                                                    required=True,
                                                    help_text='The distance function used to calculate the cost between values.',
                                                    style={'template': 'vadetisweb/parts/input/select_input.html'})
    row_standardized = serializers.BooleanField(initial=True, label='Apply Row Standardization', required=False,
                                                help_text='Determines if row standardization is applied to the correlation values',
                                                style={'template': 'vadetisweb/parts/input/text_input.html'})
    time_range = TimeRangeChoiceField(required=True)
    maximize_score = MaximizeScoreChoiceField(required=True)
    range_start = serializers.IntegerField(required=True, min_value=0,
                                           style={'template': 'vadetisweb/parts/input/hidden_input.html'})
    range_end = serializers.IntegerField(required=True, min_value=0,
                                         style={'template': 'vadetisweb/parts/input/hidden_input.html'})


class GeographicDistanceSerializer(CorrelationSerializer):
    """
    The serializer for the parameters for geographical correlation algorithm
    """
    geo_distance_function = serializers.ChoiceField(choices=GEO_DISTANCE, required=True,
                                                    help_text='The geographic distance function used for the calculation.',
                                                    style={'template': 'vadetisweb/parts/input/select_input.html'})
    time_range = serializers.ChoiceField(label='Time Range', choices=TIME_RANGE, required=True,
                                         help_text='The time range to apply anomaly detection',
                                         style={'template': 'vadetisweb/parts/input/select_input.html'})
    maximize_score = serializers.ChoiceField(label='Maximize Score', choices=ANOMALY_DETECTION_SCORE_TYPES,
                                             required=True,
                                             help_text='Define which score you want to maximize for the results. In order to achive the best score out of this selection, the most appropiate threshold value will be selected. You can further change the threshold after computation.',
                                             style={'template': 'vadetisweb/parts/input/select_input.html'})
    range_start = serializers.IntegerField(required=True, min_value=0,
                                           style={'template': 'vadetisweb/parts/input/hidden_input.html'})
    range_end = serializers.IntegerField(required=True, min_value=0,
                                         style={'template': 'vadetisweb/parts/input/hidden_input.html'})

    def __init__(self, *args, **kwargs):
        #post_data = args[0]
        super(GeographicDistanceSerializer, self).__init__(*args, **kwargs)
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
