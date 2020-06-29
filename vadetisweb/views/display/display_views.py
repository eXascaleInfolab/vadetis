from rest_framework import status
from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response

from django.shortcuts import redirect
from django.contrib import messages

from vadetisweb.models import DataSet
from vadetisweb.utils import get_highcharts_range_button_preselector
from vadetisweb.factory import dataset_not_found_msg
from vadetisweb.parameters import SYNTHETIC, REAL_WORLD
from vadetisweb.serializers.dataset.display_dataset_serializer import DisplayDatasetSearchSerializer


class DisplaySyntheticDatasets(APIView):
    """
    View for synthetic datasets
    """
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'vadetisweb/display/synthetic/datasets.html'

    def get(self, request):
        search_serializer = DisplayDatasetSearchSerializer()

        return Response({ 'search_serializer' : search_serializer }, status=status.HTTP_200_OK)


class DisplayRealWorldDatasets(APIView):
    """
    View for real world datasets
    """
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'vadetisweb/display/real-world/datasets.html'

    def get(self, request):
        search_serializer = DisplayDatasetSearchSerializer()

        return Response({ 'search_serializer' : search_serializer }, status=status.HTTP_200_OK)


class DisplaySyntheticDataset(APIView):
    """
    View for a single synthetic dataset
    """
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'vadetisweb/display/synthetic/dataset.html'

    def get(self, request, dataset_id):
        try:
            dataset = DataSet.objects.filter(id=dataset_id, public=True, type=SYNTHETIC).first()
            if dataset is None:
                messages.error(request, dataset_not_found_msg(dataset_id))
                return redirect('vadetisweb:display_synthetic_datasets')

            selected_button = get_highcharts_range_button_preselector(dataset.frequency)

            return Response({
                'dataset': dataset,
                'time_series_info' : {},
                'selected_button': selected_button
            }, status=status.HTTP_200_OK)

        except DataSet.DoesNotExist:
            messages.error(request, dataset_not_found_msg(dataset_id))
            return redirect('vadetisweb:display_synthetic_datasets')


class DisplayRealWorldDataset(APIView):
    """
    View for a single real world dataset
    """
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'vadetisweb/display/real-world/dataset.html'

    def get(self, request, dataset_id):
        try:
            dataset = DataSet.objects.filter(id=dataset_id, public=True, type=REAL_WORLD).first()
            if dataset is None:
                messages.error(request, dataset_not_found_msg(dataset_id))
                return redirect('vadetisweb:display_real_world_datasets')

            selected_button = get_highcharts_range_button_preselector(dataset.frequency)

            return Response({
                'dataset': dataset,
                'selected_button': selected_button
            }, status=status.HTTP_200_OK)

        except DataSet.DoesNotExist:
            messages.error(request, dataset_not_found_msg(dataset_id))
            return redirect('vadetisweb:display_real_world_datasets')


class DisplaySyntheticTrainingDataset(APIView):
    """
    View for a single synthetic training dataset
    """
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'vadetisweb/display/synthetic/training_dataset.html'

    def get(self, request, dataset_id, training_dataset_id):
        try:
            training_dataset = DataSet.objects.filter(id=training_dataset_id, main_dataset_id=dataset_id, public=True, type=SYNTHETIC).first()
            if training_dataset is None:
                messages.error(request, dataset_not_found_msg(dataset_id))
                return redirect('vadetisweb:display_synthetic_datasets')

            selected_button = get_highcharts_range_button_preselector(training_dataset.frequency)

            return Response({
                'dataset': training_dataset.main_dataset,
                'training_dataset': training_dataset,
                'selected_button': selected_button
            }, status=status.HTTP_200_OK)

        except DataSet.DoesNotExist:
            messages.error(request, dataset_not_found_msg(dataset_id))
            return redirect('vadetisweb:display_synthetic_datasets')


class DisplayRealWorldTrainingDataset(APIView):
    """
    View for a single real world training dataset
    """
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'vadetisweb/display/real-world/training_dataset.html'

    def get(self, request, dataset_id, training_dataset_id):
        try:
            training_dataset = DataSet.objects.filter(id=training_dataset_id, main_dataset_id=dataset_id, public=True, type=REAL_WORLD).first()
            if training_dataset is None:
                messages.error(request, dataset_not_found_msg(dataset_id))
                return redirect('vadetisweb:display_real_world_datasets')

            selected_button = get_highcharts_range_button_preselector(training_dataset.frequency)

            return Response({
                'dataset': training_dataset.main_dataset,
                'training_dataset': training_dataset,
                'selected_button': selected_button
            }, status=status.HTTP_200_OK)

        except DataSet.DoesNotExist:
            messages.error(request, dataset_not_found_msg(dataset_id))
            return redirect('vadetisweb:display_real_world_datasets')