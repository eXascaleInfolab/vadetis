from rest_framework import status
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.parsers import MultiPartParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.settings import api_settings

from django.contrib import messages

from vadetisweb.models import DataSet
from vadetisweb.serializers import AnomalyInjectionSerializer, MessageSerializer
from vadetisweb.algorithms import anomaly_injection
from vadetisweb.utils import get_dataset_with_marker_json, strToBool, get_settings, json_message_utils


class AnomalyInjectionFormView(APIView):
    """
    Request anomaly injection form
    """
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    parser_classes = [MultiPartParser]
    template_name = 'vadetisweb/parts/forms/anomaly_detection_serializer_form.html'

    def post(self, request, dataset_id, format=None):

        try:
            dataset = DataSet.objects.get(id=dataset_id)
            serializer = AnomalyInjectionSerializer(data=request.data)

            if serializer.is_valid() and request.accepted_renderer.format == 'json':  # requested format is json
                type = request.GET.get('type', 'raw')
                show_anomaly = strToBool(request.query_params.get('show_anomaly', 'true'))
                data = {}
                settings = get_settings(request)
                df_inject, df_inject_class = anomaly_injection(dataset, serializer.data)

                data['series'] = get_dataset_with_marker_json(dataset, df_inject, df_inject_class, type, show_anomaly, settings)
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
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
