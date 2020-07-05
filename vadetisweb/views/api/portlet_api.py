from rest_framework import status
from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema

from django.urls import reverse

from vadetisweb.serializers import ImagePortletSerializer, BasePortletSerializer, ThresholdSerializer, InjectionSerializer


class InjectionFormPortlet(APIView):
    """
    API for a injection form portlet
    """
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    template_name = 'vadetisweb/parts/portlet/serializer_portlet.html'

    @swagger_auto_schema(request_body=BasePortletSerializer)
    def post(self, request, format=None):
        portlet_serializer = BasePortletSerializer(data=request.data)

        if portlet_serializer.is_valid() and request.accepted_renderer.format == 'html':  # rendered template:
            validated_data = portlet_serializer.validated_data
            injection_serializer = InjectionSerializer()
            return Response({
                'id': validated_data['id'],
                'title': validated_data['title'],
                'serializer_formid' : 'threshold_form',
                'serializer_url' : reverse('vadetisweb:injection_anomaly'),
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
