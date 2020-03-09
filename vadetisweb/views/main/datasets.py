import urllib
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response

from django.shortcuts import redirect, reverse
from django.contrib import messages

from vadetisweb.models import DataSet
from vadetisweb.serializers import AlgorithmSerializer, ThresholdSerializer, AnomalyInjectionSerializer
from vadetisweb.utils import get_settings, get_highcharts_range_button_preselector, get_conf, is_valid_conf
from vadetisweb.factory import dataset_not_found_msg
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
            injection_serializer = AnomalyInjectionSerializer()

            return Response({
                'dataset': dataset,
                'selected_button': selected_button,
                'settings' : settings,
                'serializer': serializer,
                'injection_serializer' : injection_serializer,
            }, status=status.HTTP_200_OK)

        except DataSet.DoesNotExist:
            messages.error(request, dataset_not_found_msg(dataset_id))
            return redirect('vadetisweb:synthetic_datasets')


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
            messages.error(request, dataset_not_found_msg(dataset_id))
            return redirect('vadetisweb:synthetic_datasets')


class RealWorldDataset(APIView):
    """
    View for a single real world dataset
    """
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'vadetisweb/datasets/real-world/dataset.html'

    def get(self, request, dataset_id):
        try:
            dataset = DataSet.objects.get(id=dataset_id)
            if dataset.type != REAL_WORLD:
                return redirect('vadetisweb:real_world_datasets')

            selected_button = get_highcharts_range_button_preselector(dataset.frequency)
            settings = get_settings(request)

            serializer = AlgorithmSerializer()
            injection_serializer = AnomalyInjectionSerializer()

            return Response({
                'dataset': dataset,
                'selected_button': selected_button,
                'settings' : settings,
                'serializer': serializer,
                'injection_serializer' : injection_serializer,
            }, status=status.HTTP_200_OK)

        except DataSet.DoesNotExist:
            messages.error(request, dataset_not_found_msg(dataset_id))
            return redirect('vadetisweb:real_world_datasets')
