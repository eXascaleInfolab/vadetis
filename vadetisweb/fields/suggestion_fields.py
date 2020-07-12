from rest_framework import serializers
from drf_yasg import openapi


class ConfJsonField(serializers.JSONField):
    """
        JSON Field to format the used configuration for suggestion.
    """

    class Meta:
        swagger_schema_fields = {
            'type': openapi.TYPE_OBJECT,
            'properties': {
                'time_series': openapi.Schema(
                    title='time_series',
                    type=openapi.TYPE_INTEGER,
                ),
                'training_dataset': openapi.Schema(
                    title='training_dataset',
                    type=openapi.TYPE_INTEGER,
                ),
                'window_size': openapi.Schema(
                    title='window_size',
                    type=openapi.TYPE_INTEGER,
                ),
                'normalize': openapi.Schema(
                    title='normalize',
                    type=openapi.TYPE_BOOLEAN,
                ),
                'dtw_distance_function': openapi.Schema(
                    title='dtw_distance_function',
                    type=openapi.TYPE_STRING,
                ),
                'delta': openapi.Schema(
                    title='delta',
                    type=openapi.TYPE_NUMBER,
                ),
                'n_components': openapi.Schema(
                    title='n_components',
                    type=openapi.TYPE_INTEGER,
                ),
                'train_size': openapi.Schema(
                    title='train_size',
                    type=openapi.TYPE_NUMBER,
                ),
                'random_seed': openapi.Schema(
                    title='random_seed',
                    type=openapi.TYPE_INTEGER,
                ),
                'n_init': openapi.Schema(
                    title='n_init',
                    type=openapi.TYPE_INTEGER,
                ),
                'kernel': openapi.Schema(
                    title='kernel',
                    type=openapi.TYPE_STRING,
                ),
                'gamma': openapi.Schema(
                    title='gamma',
                    type=openapi.TYPE_NUMBER,
                ),
                'nu': openapi.Schema(
                    title='nu',
                    type=openapi.TYPE_NUMBER,
                ),
                'bootstrap': openapi.Schema(
                    title='bootstrap',
                    type=openapi.TYPE_BOOLEAN,
                ),
                'n_estimators': openapi.Schema(
                    title='n_estimators',
                    type=openapi.TYPE_INTEGER,
                ),
                'time_range': openapi.Schema(
                    title='time_range',
                    type=openapi.TYPE_STRING,
                ),
                'maximize_score': openapi.Schema(
                    title='maximize_score',
                    type=openapi.TYPE_STRING,
                ),
                'range_start': openapi.Schema(
                    title='range_start',
                    type=openapi.TYPE_INTEGER,
                ),
                'range_end': openapi.Schema(
                    title='range_end',
                    type=openapi.TYPE_INTEGER,
                ),
            },
            'required': ['maximize_score', 'time_range', 'range_start', 'range_end']
        }

    def __init__(self, **kwargs):
        super(ConfJsonField, self).__init__(**kwargs)


class SuggestionScoresJsonField(serializers.JSONField):
    """
        JSON Field to format the resulting scores for suggestion.
    """
    class Meta:
        swagger_schema_fields = {
            'type': openapi.TYPE_OBJECT,
            'properties': {
                'scores': openapi.Schema(
                    title='scores',
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'algorithm': openapi.Schema(
                                title='algorithm',
                                type=openapi.TYPE_STRING,
                            ),
                            'accuracy': openapi.Schema(
                                title='accuracy',
                                type=openapi.TYPE_STRING,
                            ),
                            'f1_score': openapi.Schema(
                                title='f1_score',
                                type=openapi.TYPE_STRING,
                            ),
                            'precision': openapi.Schema(
                                title='precision',
                                type=openapi.TYPE_STRING,
                            ),
                            'recall': openapi.Schema(
                                title='recall',
                                type=openapi.TYPE_STRING,
                            ),
                        },
                        required=['algorithm', 'accuracy', 'f1_score', 'precision', 'recall'],
                    )
                ),
            },
            'required': ['scores']
        }

    def __init__(self, **kwargs):
        super(SuggestionScoresJsonField, self).__init__(**kwargs)
