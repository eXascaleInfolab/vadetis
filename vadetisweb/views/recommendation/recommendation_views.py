from rest_framework import status
from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response

from django.shortcuts import redirect
from django.contrib import messages
from django.db.models import Q

from vadetisweb.models import DataSet
from vadetisweb.utils import get_highcharts_range_button_preselector, q_shared_or_user_is_owner
from vadetisweb.factory import dataset_not_found_msg
from vadetisweb.parameters import SYNTHETIC, REAL_WORLD
from vadetisweb.serializers.dataset.recommendation_dataset_serializer import RecommendationDatasetSearchSerializer
from vadetisweb.serializers.recommendation_serializers import RecommendationSerializer

class RecommendationSyntheticDatasets(APIView):
    """
    View for synthetic datasets
    """
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'vadetisweb/recommendation/synthetic/datasets.html'

    def get(self, request):
        search_serializer = RecommendationDatasetSearchSerializer()
        return Response({ 'search_serializer' : search_serializer }, status=status.HTTP_200_OK)


class RecommendationRealWorldDatasets(APIView):
    """
    View for real world datasets
    """
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'vadetisweb/recommendation/real-world/datasets.html'

    def get(self, request):
        search_serializer = RecommendationDatasetSearchSerializer()

        return Response({ 'search_serializer' : search_serializer }, status=status.HTTP_200_OK)


class RecommendationSyntheticDataset(APIView):
    """
    View for a single synthetic dataset
    """
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'vadetisweb/recommendation/synthetic/dataset.html'

    def get(self, request, dataset_id):
        dataset = DataSet.objects.filter(Q(id=dataset_id, type=SYNTHETIC),
                                         q_shared_or_user_is_owner(request)).first()
        if dataset is None:
            messages.error(request, dataset_not_found_msg(dataset_id))
            return redirect('vadetisweb:recommendation_synthetic_datasets')

        recommendation_serializer = RecommendationSerializer(context={'dataset': dataset})
        selected_button = get_highcharts_range_button_preselector(dataset.granularity)

        return Response({
            'dataset': dataset,
            'selected_button': selected_button,
            'recommendation_serializer' : recommendation_serializer,
        }, status=status.HTTP_200_OK)


class RecommendationRealWorldDataset(APIView):
    """
    View for a single real world dataset
    """
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'vadetisweb/recommendation/real-world/dataset.html'

    def get(self, request, dataset_id):
        dataset = DataSet.objects.filter(Q(id=dataset_id, type=REAL_WORLD),
                                         q_shared_or_user_is_owner(request)).first()
        if dataset is None:
            messages.error(request, dataset_not_found_msg(dataset_id))
            return redirect('vadetisweb:recommendation_real_world_datasets')

        recommendation_serializer = RecommendationSerializer(context={'dataset': dataset})
        selected_button = get_highcharts_range_button_preselector(dataset.granularity)

        return Response({
            'dataset': dataset,
            'selected_button' : selected_button,
            'recommendation_serializer' : recommendation_serializer,
        }, status=status.HTTP_200_OK)