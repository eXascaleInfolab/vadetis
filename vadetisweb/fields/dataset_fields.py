from rest_framework import serializers
from drf_yasg import openapi

from vadetisweb.models import DataSet


class MainDatasetField(serializers.PrimaryKeyRelatedField):
    def get_queryset(self):
        request = self.context.get('request', None)
        user = request.user
        return DataSet.objects.filter(owner=user, training_data=False)

    def display_value(self, instance):
        return instance.title


class DatasetJsonField(serializers.JSONField):
    """
        JSON Field to format the values of a dataset
    """
    class Meta:
        swagger_schema_fields = {
            'type': openapi.TYPE_OBJECT,
            'properties': {
                'series': openapi.Schema(
                    title='series',
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'id': openapi.Schema(
                                title='id',
                                type=openapi.TYPE_INTEGER,
                            ),
                            'name': openapi.Schema(
                                title='name',
                                type=openapi.TYPE_STRING,
                            ),
                            'unit': openapi.Schema(
                                title='unit',
                                type=openapi.TYPE_STRING,
                            ),
                            'is_spatial': openapi.Schema(
                                title='is_spatial',
                                type=openapi.TYPE_BOOLEAN,
                            ),
                            'type': openapi.Schema(
                                title='type',
                                type=openapi.TYPE_STRING,
                            ),
                            'dashStyle': openapi.Schema(
                                title='dashStyle',
                                type=openapi.TYPE_STRING,
                            ),
                            'data' : openapi.Schema(
                                title='data',
                                type=openapi.TYPE_ARRAY,
                                items=openapi.Schema(
                                    type=openapi.TYPE_OBJECT,
                                    properties={
                                        'x': openapi.Schema(
                                            title='x',
                                            type=openapi.TYPE_NUMBER,
                                        ),
                                        'y': openapi.Schema(
                                            title='y',
                                            type=openapi.TYPE_NUMBER,
                                        ),
                                        'class': openapi.Schema(
                                            title='class',
                                            type=openapi.TYPE_INTEGER,
                                            default=0
                                        ),
                                        'score': openapi.Schema(
                                            title='score',
                                            type=openapi.TYPE_NUMBER,
                                        ),
                                    },
                                    required=['x', 'y', 'class'],
                                )
                            ),
                        },
                        required=['id', 'type', 'data']
                    ),
                ),
            },
            'required': ['series']
        }
