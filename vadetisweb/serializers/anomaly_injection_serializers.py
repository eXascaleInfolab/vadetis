from rest_framework import serializers

from vadetisweb.fields import *
from vadetisweb.parameters import ANOMALY_INJECTION_TYPES


class AnomalyInjectionSerializer(serializers.Serializer):
    """
    The stochastic duration of a normal event or an anomalous event is specified by a lower bound and an
    upper bound. We randomly choose a duration from the specified range whenever a normal or an anomalous event occurs.

    The probability of an anomalous event specifies how likely an anomalous event may occur. The
    probability is determined by a nominator and a denominator.
    """

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

    anomaly_factor = serializers.IntegerField(label='Factor', initial=10, min_value=2,
                                              required=True,
                                              help_text='The factor that is used to define the deviation of the normal data.',
                                              style={'template': 'vadetisweb/parts/input/text_input.html',
                                                     'step': 'number', 'min': 2,
                                                     'help_text_in_popover': True})

    normal_lowerbound_duration = serializers.IntegerField(label='Normal lower bound', initial=50, min_value=1,
                                                          required=True,
                                                          help_text='The lower bound for duration of a normal event.',
                                                          style={'template': 'vadetisweb/parts/input/text_input.html',
                                                                 'step': 'number', 'min': 1,
                                                                 'help_text_in_popover': True})

    normal_upperbound_duration = serializers.IntegerField(label='Normal upper bound', initial=500, min_value=1,
                                                          required=True,
                                                          help_text='The upper bound for duration of a normal event.',
                                                          style={'template': 'vadetisweb/parts/input/text_input.html',
                                                                 'step': 'number', 'min': 1,
                                                                 'help_text_in_popover': True})

    probability = serializers.FloatField(label='Probability', initial=0.1, min_value=0.0000001, max_value=1,
                                         required=True,
                                         help_text='The probability for an anomalous event. '
                                                   'Should be in the interval (0, 1].',
                                         style={'template': 'vadetisweb/parts/input/text_input.html', 'step': 'any',
                                                'min': 0.0000001, 'max': 1,
                                                'help_text_in_popover': True})

    anomaly_lowerbound_duration = serializers.IntegerField(label='Anomalous lower bound', initial=5, min_value=1,
                                                           required=True,
                                                           help_text='The lower bound for duration of an anomalous event.',
                                                           style={'template': 'vadetisweb/parts/input/text_input.html',
                                                                  'step': 'number', 'min': 1,
                                                                  'help_text_in_popover': True})

    anomaly_upperbound_duration = serializers.IntegerField(label='Anomalous upper bound', initial=10, min_value=1,
                                                           required=True,
                                                           help_text='The upper bound for duration of an anomalous event.',
                                                           style={'template': 'vadetisweb/parts/input/text_input.html',
                                                                  'step': 'number', 'min': 1,
                                                                  'help_text_in_popover': True})

    def __init__(self, *args, **kwargs):
        super(AnomalyInjectionSerializer, self).__init__(*args, **kwargs)
