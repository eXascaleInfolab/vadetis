from rest_framework import status
from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema

from vadetisweb.serializers import ImagePortletSerializer, ScorePortletSerializer


class ImagePortlet(APIView):
    """
    API for a portlet
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
    API for a portlet
    """
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    template_name = 'vadetisweb/parts/portlet/score_portlet.html'

    @swagger_auto_schema(request_body=ScorePortletSerializer)
    def post(self, request, format=None):
        portlet_serializer = ScorePortletSerializer(data=request.data)

        if portlet_serializer.is_valid() and request.accepted_renderer.format == 'html':  # rendered template:
            validated_data = portlet_serializer.validated_data
            return Response({
                'id': validated_data['id'],
                'title': validated_data['title'],
            }, status=status.HTTP_200_OK)

        else:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
