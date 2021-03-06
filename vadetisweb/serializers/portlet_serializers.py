from rest_framework import serializers

from vadetisweb.fields import ConfJsonField, RecommendationScoresJsonField


class BasePortletSerializer(serializers.Serializer):
    id = serializers.CharField(required=True)
    title = serializers.CharField(required=True)


class ImagePortletSerializer(BasePortletSerializer):
    content_id = serializers.CharField(required=True)
    content_class = serializers.CharField(required=False)


class RecommendationPortletSerializer(BasePortletSerializer):
    conf = ConfJsonField(required=True, initial=None, binary=False, encoder=None)

    threshold = serializers.FloatField(required=True)
    img_1_id = serializers.CharField(required=True)
    img_2_id = serializers.CharField(required=True)
    content_class = serializers.CharField(required=False)


class RecommendationSummaryPortletSerializer(BasePortletSerializer):
    scores = RecommendationScoresJsonField(required=True, initial=None, binary=False, encoder=None)