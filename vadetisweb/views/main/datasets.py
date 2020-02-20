import urllib
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response

from django.shortcuts import redirect, reverse
from django.contrib import messages

from vadetisweb.models import DataSet
from vadetisweb.serializers import AlgorithmSerializer, ThresholdSerializer
from vadetisweb.utils import get_settings, get_highcharts_range_button_preselector, get_conf, is_valid_conf
from vadetisweb.parameters import SYNTHETIC, REAL_WORLD

class SyntheticDatasets(APIView):
    """
    View for synthetic datasets
    """
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'vadetisweb/datasets/synthetic/datasets.html'

    def get(self, request):
        return Response(status=status.HTTP_200_OK)


class RealWorldDatasets(APIView):
    """
    View for real world datasets
    """
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'vadetisweb/datasets/real-world/datasets.html'

    def get(self, request):
        return Response(status=status.HTTP_200_OK)


class SyntheticDataset(APIView):
    """
    View for a single synthetic dataset
    """
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'vadetisweb/datasets/synthetic/dataset.html'

    def get(self, request, dataset_id):
        try:
            dataset = DataSet.objects.get(id=dataset_id)
            if dataset.type != SYNTHETIC:
                return redirect('vadetisweb:synthetic_datasets')

            selected_button = get_highcharts_range_button_preselector(dataset.frequency)
            settings = get_settings(request)
            serializer = AlgorithmSerializer()

            return Response({
                'dataset': dataset,
                'selected_button': selected_button,
                'settings' : settings,
                'serializer': serializer,
            }, status=status.HTTP_200_OK)

        except DataSet.DoesNotExist:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)


class SyntheticDatasetPerformAnomalyDetection(APIView):
    """
    View for performed anomaly detection on a synthetic dataset
    """
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'vadetisweb/datasets/synthetic/dataset_perform.html'

    def get(self, request, dataset_id):
        try:
            dataset = DataSet.objects.get(id=dataset_id)
            settings = get_settings(request)
            selected_button = get_highcharts_range_button_preselector(dataset.frequency)
            conf = get_conf(request)

            if not is_valid_conf(conf):
                message = 'Invalid configuration supplied!'
                messages.error(request, message)
                return redirect(reverse('vadetisweb:synthetic_dataset', args=[dataset.id]))

            else:
                conf_params = urllib.parse.urlencode(conf)
                serializer = ThresholdSerializer()
                return Response({'is_synthetic': True, 'conf_params': conf_params, 'conf': conf,
                                 'dataset': dataset,
                                 'settings': settings,
                                 'selected_button': selected_button,
                                 'serializer': serializer}, status=status.HTTP_200_OK)

        except DataSet.DoesNotExist:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)


class RealWorldDataset(APIView):
    """
    View for a single real world dataset
    """
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'vadetisweb/datasets/real-world/dataset.html'

    def get(self, request, dataset_id):
        dataset = DataSet.objects.get(id=dataset_id)

        return Response({
            'dataset': dataset,
        }, status=status.HTTP_200_OK)
