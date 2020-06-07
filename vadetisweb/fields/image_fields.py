from rest_framework import serializers
from drf_yasg import openapi


class CnfMatrixJsonField(serializers.JSONField):
    """
        A JSON Field to transmit a cnf matrix [[TN,FP],[FN,TP]]
    """

    class Meta:
        swagger_schema_fields = {
            'type': openapi.TYPE_ARRAY,
            'items': openapi.Items(
                type=openapi.TYPE_ARRAY,
                items=openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                ),
                properties={
                    'minItems' : 2,
                    'maxItems' : 2
                }
            ),
            'properties' : {
                'minItems': 2,
                'maxItems': 2
            }
        }

    def __init__(self, **kwargs):
        super(CnfMatrixJsonField, self).__init__(**kwargs)


class ThresholdsScoresJsonField(serializers.JSONField):
    """
        A JSON Field to transmit a threshold scores values
    """

    class Meta:
        swagger_schema_fields = {
            'type': openapi.TYPE_OBJECT,
            'properties': {
                'thresholds': openapi.Schema(
                    title='thresholds',
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_NUMBER
                    )
                ),
                'threshold_scores': openapi.Schema(
                    title='threshold_scores',
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(
                            type=openapi.TYPE_NUMBER,
                        ),
                        minItems=4,
                        maxItems=4
                    ),
                ),
            },
            'required': ['thresholds', 'threshold_scores']
        }

    def __init__(self, **kwargs):
        super(ThresholdsScoresJsonField, self).__init__(**kwargs)