from rest_framework import status
from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema

from django.urls import reverse
from django.db.models import Q
from django.contrib import messages

from vadetisweb.utils import q_public_or_user_is_owner, get_settings
from vadetisweb.serializers.portlet_serializers import *
from vadetisweb.serializers import ThresholdSerializer, InjectionSerializer
from vadetisweb.models import DataSet
from vadetisweb.factory import dataset_not_found_msg


class InjectionFormPortlet(APIView):
    """
    API for a injection form portlet
    """
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    template_name = 'vadetisweb/parts/portlet/serializer_portlet.html'

    @swagger_auto_schema(request_body=BasePortletSerializer)
    def post(self, request, dataset_id, format=None):
        portlet_serializer = BasePortletSerializer(data=request.data)

        dataset = DataSet.objects.filter(Q(id=dataset_id),
                                         q_public_or_user_is_owner(request)).first()
        if dataset is None:
            messages.error(request, dataset_not_found_msg(dataset_id))
            response = Response({}, status=status.HTTP_404_NOT_FOUND)
            response['Location'] = reverse('vadetisweb:index')
            return response

        if portlet_serializer.is_valid() and request.accepted_renderer.format == 'html':  # rendered template:
            validated_data = portlet_serializer.validated_data
            injection_serializer = InjectionSerializer(context={'dataset_selected': dataset_id, 'request' : request})
            return Response({
                'id': validated_data['id'],
                'title': validated_data['title'],
                'serializer_formid' : 'anomaly_injection_form',
                'serializer_url' : reverse('vadetisweb:injection_anomaly', args=[dataset.id]),
                'serializer' : injection_serializer,
                'serializer_submit_label' : 'Update',
            }, status=status.HTTP_200_OK)

        else:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)


class ThresholdFormPortlet(APIView):
    """
    API for a threshold form portlet
    """
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    template_name = 'vadetisweb/parts/portlet/threshold_serializer_portlet.html'

    @swagger_auto_schema(request_body=BasePortletSerializer)
    def post(self, request, format=None):
        portlet_serializer = BasePortletSerializer(data=request.data)

        if portlet_serializer.is_valid() and request.accepted_renderer.format == 'html':  # rendered template:
            validated_data = portlet_serializer.validated_data
            threshold_serializer = ThresholdSerializer()
            return Response({
                'id': validated_data['id'],
                'title': validated_data['title'],
                'serializer_formid' : 'threshold_form',
                'serializer_url' : reverse('vadetisweb:threshold_update_json'),
                'serializer' : threshold_serializer,
                'serializer_submit_label' : 'Update',
            }, status=status.HTTP_200_OK)

        else:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)


class ImagePortlet(APIView):
    """
    API for a image portlet
    """
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    template_name = 'vadetisweb/parts/portlet/image_portlet.html'

    @swagger_auto_schema(request_body=ImagePortletSerializer)
    def post(self, request, format=None):
        portlet_serializer = ImagePortletSerializer(data=request.data)

        if portlet_serializer.is_valid() and request.accepted_renderer.format == 'html':  # rendered template:
            validated_data = portlet_serializer.validated_data
            return Response({
                'id': validated_data['id'],
                'title': validated_data['title'],
                'content_id': validated_data['content_id'],
                'content_class': validated_data['content_class'],
            }, status=status.HTTP_200_OK)

        else:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)


class ScorePortlet(APIView):
    """
    API for score gauges portlet
    """
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    template_name = 'vadetisweb/parts/portlet/score_portlet.html'

    @swagger_auto_schema(request_body=BasePortletSerializer)
    def post(self, request, format=None):
        portlet_serializer = BasePortletSerializer(data=request.data)

        if portlet_serializer.is_valid() and request.accepted_renderer.format == 'html':  # rendered template:
            validated_data = portlet_serializer.validated_data
            return Response({
                'id': validated_data['id'],
                'title': validated_data['title'],
            }, status=status.HTTP_200_OK)

        else:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)


class SuggestionPortlet(APIView):
    """
    API for a suggestion portlet
    """
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    template_name = 'vadetisweb/parts/portlet/suggestion_portlet.html'

    @swagger_auto_schema(request_body=SuggestionPortletSerializer)
    def post(self, request, format=None):
        portlet_serializer = SuggestionPortletSerializer(data=request.data)

        if portlet_serializer.is_valid() and request.accepted_renderer.format == 'html':  # rendered template:
            validated_data = portlet_serializer.validated_data

            settings = get_settings(request)
            round_digits = settings['round_digits']
            threshold = round(validated_data['threshold'], round_digits)

            return Response({
                'id': validated_data['id'],
                'title': validated_data['title'],
                'conf': validated_data['conf'],
                'threshold': threshold,
                'img_1_id': validated_data['img_1_id'],
                'img_2_id': validated_data['img_2_id'],
                'content_class': validated_data['content_class'],
            }, status=status.HTTP_200_OK)

        else:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)