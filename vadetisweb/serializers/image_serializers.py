from vadetisweb.fields.image_fields import *


class CnfImageSerializer(serializers.Serializer):
    """

    """
    cnf = CnfMatrixJsonField()


class ThresholdsScoresImageSerializer(serializers.Serializer):
    """

    """
    plot_data = ThresholdsScoresJsonField()