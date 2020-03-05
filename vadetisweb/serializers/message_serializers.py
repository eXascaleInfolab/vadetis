from rest_framework import serializers

class MessageSerializer(serializers.Serializer):
    """
        A message to be transferred with ajax as port of an JSON, similar to django's own message system
    """
    level = serializers.IntegerField()
    level_tag = serializers.CharField()
    message = serializers.CharField()
    extra_tags = serializers.CharField()
