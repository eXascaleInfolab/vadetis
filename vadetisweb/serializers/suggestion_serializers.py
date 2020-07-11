from rest_framework import serializers

from vadetisweb.fields import *
from vadetisweb.utils import get_detection_choices


class SuggestionSerializer(serializers.Serializer):

    empty_choice = ('', '----')
    # choices are loaded from context
    algorithm = serializers.ChoiceField(choices=empty_choice, required=True,
                                        style={'template': 'vadetisweb/parts/input/select_input.html',
                                               'help_text_in_popover': True})

    def __init__(self, *args, **kwargs):
        super(SuggestionSerializer, self).__init__(*args, **kwargs)
        dataset = self.context.get('dataset', None)
        self.fields['algorithm'].choices = get_detection_choices(dataset)
