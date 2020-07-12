from rest_framework import serializers

from vadetisweb.fields import *
from vadetisweb.utils import get_detection_choices


class SuggestionSerializer(serializers.Serializer):
    empty_choice = ('', '----')

    maximize_score = serializers.ChoiceField(label='Maximize Score', choices=ANOMALY_DETECTION_SCORE_TYPES,
                                             help_text='Define which score you want to maximize for the suggestions.', required=True,
                                             style={'template': 'vadetisweb/parts/input/select_input.html',
                                                    'help_text_in_popover': True})

    # choices are loaded from context
    algorithm = serializers.MultipleChoiceField(choices=empty_choice, required=True,
                                                help_text='Select the algorithms to use for the suggestion.',
                                                style={'template': 'vadetisweb/parts/input/checkbox_multiple_input.html',
                                                       'help_text_in_popover': True})

    def __init__(self, *args, **kwargs):
        super(SuggestionSerializer, self).__init__(*args, **kwargs)
        dataset = self.context.get('dataset', None)
        self.fields['algorithm'].choices = get_detection_choices(dataset, with_empty=False)
