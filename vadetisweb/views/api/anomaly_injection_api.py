from rest_framework import status
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.parsers import MultiPartParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.settings import api_settings
from drf_yasg.utils import swagger_auto_schema

from django.contrib import messages
from django.shortcuts import redirect

from vadetisweb.models import DataSet
from vadetisweb.serializers import AnomalyInjectionSerializer, MessageSerializer
from vadetisweb.algorithms import anomaly_injection
from vadetisweb.utils import get_dataset_with_marker_json, strToBool, get_settings, json_message_utils
from vadetisweb.factory import dataset_not_found_msg


class AnomalyInjectionFormView(APIView):
    """
    Request anomaly injection form
    """
    renderer_classes = [JSONRenderer]

    @swagger_auto_schema(request_body=AnomalyInjectionSerializer)
    def post(self, request, dataset_id, format=None):

        try:
            dataset = DataSet.objects.get(id=dataset_id)
            serializer = AnomalyInjectionSerializer(context={'dataset_selected': dataset_id, }, data=request.data)

            if serializer.is_valid() and request.accepted_renderer.format == 'json':  # requested format is json
                show_anomaly = strToBool(request.query_params.get('show_anomaly', 'true'))
                data = {}
                settings = get_settings(request)
                df_inject, df_inject_class = anomaly_injection(dataset, serializer.validated_data)

                data['series'] = get_dataset_with_marker_json(dataset, df_inject, df_inject_class, show_anomaly, settings)
                return Response(data, status=status.HTTP_200_OK)

            else:
                message = "Form was invalid"
                if request.accepted_renderer.format == 'json':  # requested format is json
                    json_messages = []
                    json_message_utils.error(json_messages, message)

                    # append non field form errors to message errors
                    if (api_settings.NON_FIELD_ERRORS_KEY in serializer.errors):
                        for non_field_error in serializer.errors[api_settings.NON_FIELD_ERRORS_KEY]:
                            json_message_utils.error(json_messages, non_field_error)

                    return Response({
                        'messages': MessageSerializer(json_messages, many=True).data,
                        'form_errors': serializer.errors
                    }, status=status.HTTP_400_BAD_REQUEST)

                else:  # or render html template
                    messages.error(request, message)
                    return Response({
                        'injection_serializer': serializer,
                    }, status=status.HTTP_400_BAD_REQUEST)

        except DataSet.DoesNotExist:
            messages.error(request, dataset_not_found_msg(dataset_id))
            return redirect('vadetisweb:index')
