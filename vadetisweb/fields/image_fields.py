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
