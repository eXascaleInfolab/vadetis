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


class RoundDigitsField(serializers.IntegerField):
    def __init__(self, **kwargs):
        super(RoundDigitsField, self).__init__(**kwargs)
        self.label = 'Round digits'
        self.help_text = 'Used to set the decimal places for the presentation. Note: Computation is always performed on the original data.'
        self.style = {'template': 'vadetisweb/parts/input/ion_slider_input.html',
                      'id': 'round_digits',
                      'data_type': "single",
                      'data_grid': "false",
                      'data_min': self.min_value,
                      'data_max': self.max_value,
                      'data_from': self.initial,
                      'data_step': "1",
                      'help_text_in_popover': False}
