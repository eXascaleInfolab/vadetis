from vadetisweb.fields import *
from vadetisweb.utils import get_detection_choices, get_preselected_detection_choices


class RecommendationSerializer(serializers.Serializer):
    empty_choice = ('', '----')

    maximize_score = serializers.ChoiceField(label='Maximize Score', choices=ANOMALY_DETECTION_SCORE_TYPES,
                                             help_text='Define which score you want to maximize for the recommendations.', required=True,
                                             style={'template': 'vadetisweb/parts/input/select_input.html',
                                                    'help_text_in_popover': True})

    # choices are loaded from context
    algorithm = serializers.MultipleChoiceField(choices=empty_choice, required=True,
                                                help_text='Select the algorithms to use for the recommendation. The possibilities depend on whether training data and spatial data are available or not.',
                                                style={'template': 'vadetisweb/parts/input/checkbox_multiple_input.html',
                                                       'help_text_in_popover': True})

    def __init__(self, *args, **kwargs):
        super(RecommendationSerializer, self).__init__(*args, **kwargs)
        dataset = self.context.get('dataset', None)
        if dataset is not None:
            detection_choices = get_detection_choices(dataset, with_empty=False)
            self.fields['algorithm'].choices = detection_choices
            self.fields['algorithm'].initial = get_preselected_detection_choices(detection_choices)
