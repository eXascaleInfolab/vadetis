from rest_framework import serializers

from vadetisweb.fields import *
from vadetisweb.parameters import ANOMALY_INJECTION_TYPES, ANOMALY_INJECTION_DEVIATIONS, ANOMALY_INJECTION_DEVIATION_MEDIUM, ANOMALY_INJECTION_REPETITIONS, ANOMALY_INJECTION_REPEAT_SINGLE


class AnomalyInjectionSerializer(serializers.Serializer):

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

    anomaly_repetition = serializers.ChoiceField(label='Insertion',
                                                required=False,
                                                choices=ANOMALY_INJECTION_REPETITIONS,
                                                default=ANOMALY_INJECTION_REPEAT_SINGLE,
                                                help_text='Anomalies are inserted into the selected area of the chart. Anomalies can be inserted individually or in intervals.',
                                                style={'template': 'vadetisweb/parts/input/select_input.html',
                                                       'help_text_in_popover': True})

    anomaly_deviation = serializers.ChoiceField(label='Deviation',
                                                required=False,
                                                choices=ANOMALY_INJECTION_DEVIATIONS,
                                                default=ANOMALY_INJECTION_DEVIATION_MEDIUM,
                                                help_text='The grade of deviation for anomalies from the normal data.',
                                                style={'template': 'vadetisweb/parts/input/select_input.html',
                                                       'help_text_in_popover': True})

    range_start = RangeStartHiddenIntegerField(html_id='rangeStartInjection')
    range_end = RangeEndHiddenIntegerField(html_id='rangeEndInjection')

    def __init__(self, *args, **kwargs):
        super(AnomalyInjectionSerializer, self).__init__(*args, **kwargs)
