import json
from rest_framework import serializers
from django.contrib.messages import utils, constants

LEVEL_TAGS = utils.get_level_tags()


class JsonMessage:
    """
        A message to be transferred with ajax as port of an JSON, similar to django's own message system
    """

    def __init__(self, level, message, extra_tags=None):
        self.level = int(level)
        self.level_tag = LEVEL_TAGS.get(level, '')
        self.message = message
        self.extra_tags = extra_tags

    def __eq__(self, other):
        if not isinstance(other, JsonMessage):
            return NotImplemented
        return self.level == other.level and self.message == other.message

    def __str__(self):
        return str(self.message)

    @property
    def tags(self):
        return ' '.join(tag for tag in [self.extra_tags, self.level_tag] if tag)


class MessageSerializer(serializers.Serializer):
    """
        A message to be transferred with ajax as port of an JSON, similar to django's own message system
    """
    level = serializers.IntegerField()
    level_tag = serializers.CharField()
    message = serializers.CharField()
    extra_tags = serializers.CharField()


def debug(messages, message, extra_tags=''):
    """Add a message with the ``DEBUG`` level."""
    message = JsonMessage(constants.DEBUG, message, extra_tags)
    messages.append(message)


def info(messages, message, extra_tags=''):
    """Add a message with the ``INFO`` level."""
    message = JsonMessage(constants.INFO, message, extra_tags)
    messages.append(message)


def success(messages, message, extra_tags=''):
    """Add a message with the ``SUCCESS`` level."""
    message = JsonMessage(constants.SUCCESS, message, extra_tags)
    messages.append(message)


def warning(messages, message, extra_tags=''):
    """Add a message with the ``WARNING`` level."""
    message = JsonMessage(constants.WARNING, message, extra_tags)
    messages.append(message)


def error(messages, message, extra_tags=''):
    """Add a message with the ``ERROR`` level."""
    message = JsonMessage(constants.ERROR, message, extra_tags)
    messages.append(message)
