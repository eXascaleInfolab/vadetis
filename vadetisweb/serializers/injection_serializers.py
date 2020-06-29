from rest_framework import serializers

from vadetisweb.fields import *
from vadetisweb.parameters import ANOMALY_INJECTION_TYPES, ANOMALY_INJECTION_DEVIATIONS, ANOMALY_INJECTION_DEVIATION_MEDIUM


class AnomalyInjectionSerializer(serializers.Serializer):
    """
    The stochastic duration of a normal event or an anomalous event is specified by a lower bound and an
    upper bound. We randomly choose a duration from the specified range whenever a normal or an anomalous event occurs.

    The probability of an anomalous event specifies how likely an anomalous event may occur. The
    probability is determined by a nominator and a denominator.
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
                                  help_text='The time series to inject anomalies.')

    anomaly_type = serializers.ChoiceField(label='Anomaly Type',
                                           required=True,
                                           choices=ANOMALY_INJECTION_TYPES,
                                           help_text='The type of anomalies for injection. Choose between extreme value outliers, a level or trend shift or increased variance in the data.',
                                           style={'template': 'vadetisweb/parts/input/select_input.html',
                                                  'help_text_in_popover': True})

    anomaly_deviation = serializers.ChoiceField(label='Deviation',
                                                allow_blank=False,
                                                choices=ANOMALY_INJECTION_DEVIATIONS,
                                                default=ANOMALY_INJECTION_DEVIATION_MEDIUM,
                                                help_text='The grade of deviation for anomalies from the normal data.',
                                                style={'template': 'vadetisweb/parts/input/select_input.html',
                                                       'help_text_in_popover': True})

    normal_range = IonIntegerRangeJsonField(label="Normal range", required=True,
                                            help_text='The bound for duration of a normal event.',
                                            style={'template': 'vadetisweb/parts/input/ion_slider_input.html',
                                                   'id': 'normal_range',
                                                   'data_type': "double",
                                                   'data_grid': "true",
                                                   'data_min': "100",
                                                   'data_max': "1000",
                                                   'data_from': "200",
                                                   'data_to': "800",
                                                   'help_text_in_popover': True})

    anomaly_range = IonIntegerRangeJsonField(label="Anomalous range", required=True,
                                             help_text='The bound for duration of an anomalous event.',
                                             style={'template': 'vadetisweb/parts/input/ion_slider_input.html',
                                                    'id': 'anomaly_range',
                                                    'data_type': "double",
                                                    'data_grid': "true",
                                                    'data_min': "1",
                                                    'data_max': "100",
                                                    'data_from': "10",
                                                    'data_to': "20",
                                                    'help_text_in_popover': True})

    probability = serializers.FloatField(label='Probability', initial=0.5, min_value=0, max_value=1,
                                         required=True,
                                         help_text='The probability for an anomalous event.',
                                         style={'template': 'vadetisweb/parts/input/ion_slider_input.html',
                                                'id': 'probability',
                                                'data_type': "single",
                                                'data_grid': "true",
                                                'data_min': "0",
                                                'data_max': "1",
                                                'data_from': "0.5",
                                                'data_step': "0.1",
                                                'help_text_in_popover': True})

    def __init__(self, *args, **kwargs):
        super(AnomalyInjectionSerializer, self).__init__(*args, **kwargs)
