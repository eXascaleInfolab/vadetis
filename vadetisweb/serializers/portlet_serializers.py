from rest_framework import serializers


class BasePortletSerializer(serializers.Serializer):
    id = serializers.CharField(required=True)
    title = serializers.CharField(required=True)

class ImagePortletSerializer(BasePortletSerializer):
    content_id = serializers.CharField(required=True)
    content_class = serializers.CharField(required=False)

class SuggestionPortletSerializer(BasePortletSerializer):
    maximized_score = serializers.CharField(required=True)
    threshold = serializers.FloatField(required=True)
    img_1_id = serializers.CharField(required=True)
    img_2_id = serializers.CharField(required=True)
    content_class = serializers.CharField(required=False)