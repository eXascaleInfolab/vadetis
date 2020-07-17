from django.contrib import messages
from django.db.models import Q
from django.shortcuts import redirect
from rest_framework import status
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from vadetisweb.factory import dataset_not_found_msg
from vadetisweb.models import DataSet
from vadetisweb.parameters import SYNTHETIC, REAL_WORLD
from vadetisweb.serializers import AlgorithmSerializer, ThresholdSerializer, InjectionSerializer
from vadetisweb.serializers.dataset.detection_dataset_serializer import DetectionDatasetSearchSerializer
from vadetisweb.utils import get_highcharts_range_button_preselector, q_shared_or_user_is_owner


class DetectionSyntheticDatasets(APIView):
    """
    View for synthetic datasets
    """
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'vadetisweb/detection/synthetic/datasets.html'

    def get(self, request):
        search_serializer = DetectionDatasetSearchSerializer()
        return Response({ 'search_serializer' : search_serializer }, status=status.HTTP_200_OK)


class DetectionRealWorldDatasets(APIView):
    """
    View for real world datasets
    """
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'vadetisweb/detection/real-world/datasets.html'

    def get(self, request):
        search_serializer = DetectionDatasetSearchSerializer()

        return Response({ 'search_serializer' : search_serializer }, status=status.HTTP_200_OK)


class DetectionSyntheticDataset(APIView):
    """
    View for a single synthetic dataset
    """
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'vadetisweb/detection/synthetic/dataset.html'

    def get(self, request, dataset_id):
        dataset = DataSet.objects.filter(Q(id=dataset_id, type=SYNTHETIC),
                                         q_shared_or_user_is_owner(request)).first()
        if dataset is None:
            messages.error(request, dataset_not_found_msg(dataset_id))
            return redirect('vadetisweb:detection_synthetic_datasets')

        selected_button = get_highcharts_range_button_preselector(dataset.granularity)

        detection_serializer = AlgorithmSerializer(context={'dataset': dataset})
        injection_serializer = InjectionSerializer(context={'dataset_selected': dataset_id, 'request' : request})
        threshold_serializer = ThresholdSerializer()

        return Response({
            'dataset': dataset,
            'selected_button': selected_button,
            'detection_serializer': detection_serializer,
            'injection_serializer' : injection_serializer,
            'threshold_serializer': threshold_serializer,
        }, status=status.HTTP_200_OK)


class DetectionRealWorldDataset(APIView):
    """
    View for a single real world dataset
    """
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'vadetisweb/detection/real-world/dataset.html'

    def get(self, request, dataset_id):
        dataset = DataSet.objects.filter(Q(id=dataset_id, type=REAL_WORLD),
                                         q_shared_or_user_is_owner(request)).first()
        if dataset is None:
            messages.error(request, dataset_not_found_msg(dataset_id))
            return redirect('vadetisweb:detection_real_world_datasets')

        selected_button = get_highcharts_range_button_preselector(dataset.granularity)

        detection_serializer = AlgorithmSerializer(context={'dataset': dataset})
        injection_serializer = InjectionSerializer(context={'dataset_selected': dataset_id, 'request' : request})
        threshold_serializer = ThresholdSerializer()

        return Response({
            'dataset': dataset,
            'selected_button': selected_button,
            'detection_serializer': detection_serializer,
            'injection_serializer' : injection_serializer,
            'threshold_serializer': threshold_serializer,
        }, status=status.HTTP_200_OK)
