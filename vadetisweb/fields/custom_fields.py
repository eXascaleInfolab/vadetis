from rest_framework import serializers
from drf_yasg import openapi


class IonIntegerRangeJsonField(serializers.JSONField):
    """
        A custom JSON Field to transmit a range of upper and lower value
     """

    class Meta:
        swagger_schema_fields = {
            'type': openapi.TYPE_OBJECT,
            'properties': {
                'lower': openapi.Schema(
                    title='lower',
                    type=openapi.TYPE_INTEGER,
                ),
                'upper': openapi.Schema(
                    title='upper',
                    type=openapi.TYPE_INTEGER,
                ),
            },
            'required': ['lower', 'upper']
        }

    def __init__(self, **kwargs):
        super(IonIntegerRangeJsonField, self).__init__(**kwargs)
