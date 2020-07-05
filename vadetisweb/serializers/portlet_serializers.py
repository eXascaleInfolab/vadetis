from rest_framework import serializers


class PortletSerializer(serializers.Serializer):
    id = serializers.CharField(required=True)
    title = serializers.CharField(required=True)
    content_id = serializers.CharField(required=True)
    content_class = serializers.CharField(required=False)