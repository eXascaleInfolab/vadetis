from rest_framework import serializers

from vadetisweb.fields import CnfMatrixJsonField

class CnfImageSerializer(serializers.Serializer):
    """

    """
    cnf = CnfMatrixJsonField()


class ThresholdScoreImageSerializer(serializers.Serializer):
    """

    """
    level = serializers.IntegerField()