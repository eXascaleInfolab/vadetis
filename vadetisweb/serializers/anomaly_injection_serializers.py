from rest_framework import serializers


class AnomalyInjectionSerializer(serializers.Serializer):
    """
    The stochastic duration of a normal event or an anomalous event is specified by a lower bound and an
    upper bound. We randomly choose a duration from the specified range whenever a normal or an anomalous event occurs.

    The probability of an anomalous event specifies how likely an anomalous event may occur. The
    probability is determined by a nominator and a denominator.
    """

    normal_lowerbound_duration = serializers.IntegerField(initial=100, label='Normal lower bound', min_value=1,
                                                          required=True,
                                                          help_text='The lower bound for duration of a normal event.',
                                                          style={'template': 'vadetisweb/parts/input/text_input.html',
                                                                 'step': 'number', 'min': 1})

    normal_upperbound_duration = serializers.IntegerField(initial=200, label='Normal upper bound', min_value=1,
                                                          required=True,
                                                          help_text='The upper bound for duration of a normal event.',
                                                          style={'template': 'vadetisweb/parts/input/text_input.html',
                                                                 'step': 'number', 'min': 1})

    anomaly_lowerbound_duration = serializers.IntegerField(initial=5, label='Anomalous lower bound', min_value=1,
                                                           required=True,
                                                           help_text='The lower bound for duration of an anomalous event.',
                                                           style={'template': 'vadetisweb/parts/input/text_input.html',
                                                                  'step': 'number', 'min': 1})

    anomaly_upperbound_duration = serializers.IntegerField(initial=10, label='Anomalous upper bound', min_value=1,
                                                           required=True,
                                                           help_text='The upper bound for duration of an anomalous event.',
                                                           style={'template': 'vadetisweb/parts/input/text_input.html',
                                                                  'step': 'number', 'min': 1})

    probability = serializers.FloatField(initial=0.1, label='Probability', min_value=0.0000001, max_value=1, required=True,
                                         help_text='The probability for an anomaly during an anomalous event. '
                                                   'Should be in the interval (0, 1]. If none, the default value 0.1 will be used.',
                                         style={'template': 'vadetisweb/parts/input/text_input.html', 'step': 'any',
                                                'min': 0.0000001, 'max': 1})

    def __init__(self, *args, **kwargs):
        super(AnomalyInjectionSerializer, self).__init__(*args, **kwargs)
