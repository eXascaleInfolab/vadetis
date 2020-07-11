from rest_framework import status
from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response

from django.shortcuts import redirect
from django.contrib import messages
from django.db.models import Q

from vadetisweb.models import DataSet
from vadetisweb.utils import get_highcharts_range_button_preselector, q_public_or_user_is_owner
from vadetisweb.factory import dataset_not_found_msg
from vadetisweb.parameters import SYNTHETIC, REAL_WORLD
from vadetisweb.serializers.dataset.suggestion_dataset_serializer import SuggestionDatasetSearchSerializer
from vadetisweb.serializers.suggestion_serializers import SuggestionSerializer

class SuggestionSyntheticDatasets(APIView):
    """
    View for synthetic datasets
    """
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'vadetisweb/suggestion/synthetic/datasets.html'

    def get(self, request):
        search_serializer = SuggestionDatasetSearchSerializer()
        return Response({ 'search_serializer' : search_serializer }, status=status.HTTP_200_OK)


class SuggestionRealWorldDatasets(APIView):
    """
    View for real world datasets
    """
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'vadetisweb/suggestion/real-world/datasets.html'

    def get(self, request):
        search_serializer = SuggestionDatasetSearchSerializer()

        return Response({ 'search_serializer' : search_serializer }, status=status.HTTP_200_OK)


class SuggestionSyntheticDataset(APIView):
    """
    View for a single synthetic dataset
    """
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'vadetisweb/suggestion/synthetic/dataset.html'

    def get(self, request, dataset_id):
        dataset = DataSet.objects.filter(Q(id=dataset_id, type=SYNTHETIC),
                                         q_public_or_user_is_owner(request)).first()
        if dataset is None:
            messages.error(request, dataset_not_found_msg(dataset_id))
            return redirect('vadetisweb:suggestion_synthetic_datasets')

        suggestion_serializer = SuggestionSerializer(context={'dataset': dataset})

        return Response({
            'dataset': dataset,
            'suggestion_serializer' : suggestion_serializer,
        }, status=status.HTTP_200_OK)


class SuggestionRealWorldDataset(APIView):
    """
    View for a single real world dataset
    """
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'vadetisweb/suggestion/real-world/dataset.html'

    def get(self, request, dataset_id):
        dataset = DataSet.objects.filter(Q(id=dataset_id, type=REAL_WORLD),
                                         q_public_or_user_is_owner(request)).first()
        if dataset is None:
            messages.error(request, dataset_not_found_msg(dataset_id))
            return redirect('vadetisweb:suggestion_real_world_datasets')

        suggestion_serializer = SuggestionSerializer(context={'dataset': dataset})

        return Response({
            'dataset': dataset,
            'suggestion_serializer' : suggestion_serializer,
        }, status=status.HTTP_200_OK)