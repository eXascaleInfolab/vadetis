from rest_framework import status
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.parsers import MultiPartParser
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from vadetisweb.serializers import AlgorithmSerializer
from vadetisweb.models import DataSet
from vadetisweb.utils import datatable_dataset_rows
from vadetisweb.parameters import REAL_WORLD, SYNTHETIC


class SyntheticDatasetsJson(APIView):
    """
    Request synthetic datasets
    """
    renderer_classes = [JSONRenderer]

    def get(self, request):
        data = []

        datasets = DataSet.objects.filter(type=SYNTHETIC, is_training_data=False)
        data = datatable_dataset_rows(data, datasets)

        return Response(data)


class RealWorldDatasetsJson(APIView):
    """
    Request real-world datasets
    """
    renderer_classes = [JSONRenderer]

    def get(self, request):
        data = []

        datasets = DataSet.objects.filter(type=REAL_WORLD, is_training_data=False)
        data = datatable_dataset_rows(data, datasets)

        return Response(data)


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
        return Response(status=status.HTTP_200_OK)


class RealWorldDataset(APIView):
    """
    View for a single real world dataset
    """
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'vadetisweb/datasets/real-world/dataset.html'

    def get(self, request, dataset_id):
        return Response(status=status.HTTP_200_OK)