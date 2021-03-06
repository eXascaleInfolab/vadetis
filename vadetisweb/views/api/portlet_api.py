from django.contrib import messages
from django.db.models import Q
from django.urls import reverse
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from vadetisweb.factory import dataset_not_found_msg
from vadetisweb.models import DataSet
from vadetisweb.serializers import ThresholdSerializer, InjectionSerializer
from vadetisweb.serializers.portlet_serializers import *
from vadetisweb.utils import q_shared_or_user_is_owner, get_settings, get_transformed_conf, get_recommendation


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
                                         q_shared_or_user_is_owner(request)).first()
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


class RecommendationPortlet(APIView):
    """
    API for a recommendation portlet
    """
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    template_name = 'vadetisweb/parts/portlet/recommendation_portlet.html'

    @swagger_auto_schema(request_body=RecommendationPortletSerializer)
    def post(self, request, format=None):
        portlet_serializer = RecommendationPortletSerializer(data=request.data)

        if portlet_serializer.is_valid() and request.accepted_renderer.format == 'html':  # rendered template:
            validated_data = portlet_serializer.validated_data

            threshold = round(validated_data['threshold'], 3)

            transformed_conf = get_transformed_conf(validated_data['conf'])

            return Response({
                'id': validated_data['id'],
                'title': validated_data['title'],
                'conf': transformed_conf,
                'threshold': threshold,
                'img_1_id': validated_data['img_1_id'],
                'img_2_id': validated_data['img_2_id'],
                'content_class': validated_data['content_class'],
            }, status=status.HTTP_200_OK)

        else:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)


class RecommendationSummaryPortlet(APIView):
    """
    API for a recommendation summary portlet
    """
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    template_name = 'vadetisweb/parts/portlet/recommendation_summary_portlet.html'

    @swagger_auto_schema(request_body=RecommendationSummaryPortletSerializer)
    def post(self, request, format=None):
        portlet_serializer = RecommendationSummaryPortletSerializer(data=request.data)

        if portlet_serializer.is_valid() and request.accepted_renderer.format == 'html':  # rendered template:
            validated_data = portlet_serializer.validated_data

            recommendation = get_recommendation(validated_data['scores'])

            return Response({
                'id': validated_data['id'],
                'title': validated_data['title'],
                'recommendation': recommendation,
            }, status=status.HTTP_200_OK)

        else:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)