import urllib
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response

from django.shortcuts import redirect, reverse
from django.contrib import messages

from vadetisweb.models import DataSet
from vadetisweb.serializers import AlgorithmSerializer, ThresholdSerializer, AnomalyInjectionSerializer
from vadetisweb.utils import get_settings, get_highcharts_range_button_preselector, get_conf_from_query_params, is_valid_conf
from vadetisweb.factory import dataset_not_found_msg
from vadetisweb.parameters import SYNTHETIC, REAL_WORLD


class DetectionSyntheticDatasets(APIView):
    """
    View for synthetic datasets
    """
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'vadetisweb/detection/synthetic/datasets.html'

    def get(self, request):
        return Response(status=status.HTTP_200_OK)


class DetectionRealWorldDatasets(APIView):
    """
    View for real world datasets
    """
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'vadetisweb/detection/real-world/datasets.html'

    def get(self, request):
        return Response(status=status.HTTP_200_OK)


class DetectionSyntheticDataset(APIView):
    """
    View for a single synthetic dataset
    """
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'vadetisweb/detection/synthetic/dataset.html'

    def get(self, request, dataset_id):
        try:
            dataset = DataSet.objects.get(id=dataset_id)
            if dataset.type != SYNTHETIC:
                return redirect('vadetisweb:detection_synthetic_datasets')

            selected_button = get_highcharts_range_button_preselector(dataset.frequency)

            detection_serializer = AlgorithmSerializer()
            injection_serializer = AnomalyInjectionSerializer(context={'dataset_selected': dataset_id, })
            threshold_serializer = ThresholdSerializer()

            return Response({
                'dataset': dataset,
                'selected_button': selected_button,
                'detection_serializer': detection_serializer,
                'injection_serializer' : injection_serializer,
                'threshold_serializer': threshold_serializer,
            }, status=status.HTTP_200_OK)

        except DataSet.DoesNotExist:
            messages.error(request, dataset_not_found_msg(dataset_id))
            return redirect('vadetisweb:detection_synthetic_datasets')


class DetectionRealWorldDataset(APIView):
    """
    View for a single real world dataset
    """
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'vadetisweb/detection/real-world/dataset.html'

    def get(self, request, dataset_id):
        try:
            dataset = DataSet.objects.get(id=dataset_id)
            if dataset.type != REAL_WORLD:
                return redirect('vadetisweb:detection_real_world_datasets')

            selected_button = get_highcharts_range_button_preselector(dataset.frequency)

            detection_serializer = AlgorithmSerializer()
            injection_serializer = AnomalyInjectionSerializer(context={'dataset_selected': dataset_id, })
            threshold_serializer = ThresholdSerializer()

            return Response({
                'dataset': dataset,
                'selected_button': selected_button,
                'detection_serializer': detection_serializer,
                'injection_serializer' : injection_serializer,
                'threshold_serializer': threshold_serializer,
            }, status=status.HTTP_200_OK)

        except DataSet.DoesNotExist:
            messages.error(request, dataset_not_found_msg(dataset_id))
            return redirect('vadetisweb:detection_real_world_datasets')
