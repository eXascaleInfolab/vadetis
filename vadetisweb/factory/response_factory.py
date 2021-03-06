from rest_framework import status
from rest_framework.response import Response
from rest_framework.settings import api_settings

from vadetisweb.serializers.message_serializers import MessageSerializer
from vadetisweb.utils import json_message_utils


def response_invalid_form(serializer, json_messages):

    # append non field form errors to message errors
    if (api_settings.NON_FIELD_ERRORS_KEY in serializer.errors):
        for non_field_error in serializer.errors[api_settings.NON_FIELD_ERRORS_KEY]:
            json_message_utils.error(json_messages, non_field_error)

    return Response({
        'messages': MessageSerializer(json_messages, many=True).data,
        'form_errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


def exception_message_response(e):
    message = getattr(e, 'message', str(e))
    if message is not None and message != '':
        json_messages = []
        json_message_utils.error(json_messages, getattr(e, 'message', str(e)))
        return Response({
            'status': 'error',
            'messages': MessageSerializer(json_messages, many=True).data,
        }, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({}, status=status.HTTP_400_BAD_REQUEST)