from rest_framework import status
from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from drf_yasg.utils import swagger_auto_schema

from vadetisweb.serializers import PortletSerializer


class BasePortlet(APIView):
    """
    API for a portlet
    """
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    template_name = 'vadetisweb/parts/portlet/base_portlet.html'

    @swagger_auto_schema(request_body=PortletSerializer)
    def post(self, request, format=None):
        portlet_serializer = PortletSerializer(data=request.data)

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
