from rest_framework import serializers

from vadetisweb.fields import ConfJsonField, SuggestionScoresJsonField


class BasePortletSerializer(serializers.Serializer):
    id = serializers.CharField(required=True)
    title = serializers.CharField(required=True)


class ImagePortletSerializer(BasePortletSerializer):
    content_id = serializers.CharField(required=True)
    content_class = serializers.CharField(required=False)


class SuggestionPortletSerializer(BasePortletSerializer):
    conf = ConfJsonField(required=True, initial=None, binary=False, encoder=None)

    threshold = serializers.FloatField(required=True)
    img_1_id = serializers.CharField(required=True)
    img_2_id = serializers.CharField(required=True)
    content_class = serializers.CharField(required=False)


class RecommendationPortletSerializer(BasePortletSerializer):
    scores = SuggestionScoresJsonField(required=True, initial=None, binary=False, encoder=None)