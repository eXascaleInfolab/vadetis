from rest_framework import serializers
from vadetisweb.parameters import ANOMALY_DETECTION_ALGORITHMS


class AnomalyDetectionSerializer(serializers.Serializer):

    empty_choice = ('', '----')
    ANOMALY_DETECTION_ALGORITHMS_EMPTY = (empty_choice,) + ANOMALY_DETECTION_ALGORITHMS

    algorithm = serializers.ChoiceField(choices=ANOMALY_DETECTION_ALGORITHMS_EMPTY,
                                  required=True,
                                  help_text='The type of anomaly detection algorithm')
