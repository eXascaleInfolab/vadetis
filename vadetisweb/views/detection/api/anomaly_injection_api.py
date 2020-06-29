from rest_framework import status
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.parsers import MultiPartParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.settings import api_settings
from drf_yasg.utils import swagger_auto_schema

from django.contrib import messages
from django.shortcuts import redirect
from django.db.models import Q

from vadetisweb.models import DataSet
from vadetisweb.serializers import AnomalyInjectionSerializer, MessageSerializer
from vadetisweb.algorithms import anomaly_injection
from vadetisweb.utils import dataset_to_json, strToBool, get_settings, json_message_utils, q_public_or_user_is_owner
from vadetisweb.factory import *


class AnomalyInjectionFormView(APIView):
    """
    Request anomaly injection
    """
    renderer_classes = [JSONRenderer]

    @swagger_auto_schema(request_body=AnomalyInjectionSerializer)
    def post(self, request, dataset_id, format=None):

        dataset = DataSet.objects.filter(Q(id=dataset_id),
                                         q_public_or_user_is_owner(request)).first()
        if dataset is None:
            messages.error(request, dataset_not_found_msg(dataset_id))
            return redirect('vadetisweb:index')


        serializer = AnomalyInjectionSerializer(context={'dataset_selected': dataset_id, 'request' : request }, data=request.data)

        if serializer.is_valid() and request.accepted_renderer.format == 'json':  # requested format is json
            show_anomaly = strToBool(request.query_params.get('show_anomaly', 'true'))
            data = {}
            settings = get_settings(request)
            df_inject, df_inject_class = anomaly_injection(serializer.validated_data)

            data['series'] = dataset_to_json(dataset, df_inject, df_inject_class, show_anomaly, settings, 'raw') #raw todo
            return Response(data, status=status.HTTP_200_OK)

        else:
            message = "Form was invalid"
            if request.accepted_renderer.format == 'json':  # requested format is json
                json_messages = []
                json_message_utils.error(json_messages, message)
                return invalid_form_rest_response(serializer, json_messages)

            else:  # or render html template
                messages.error(request, message)
                return Response({
                    'injection_serializer': serializer,
                }, status=status.HTTP_400_BAD_REQUEST)
