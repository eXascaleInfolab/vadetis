from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.parsers import MultiPartParser
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from vadetisweb.models import DataSet
from vadetisweb.utils import datatable_dataset_rows
from vadetisweb.parameters import REAL_WORLD, SYNTHETIC


class SyntheticDatasets(APIView):
    """
    Request synthetic datasets
    """
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    renderer_classes = [JSONRenderer]

    def get(self, request):
        data = []

        datasets = DataSet.objects.filter(type=SYNTHETIC, is_training_data=False)
        data = datatable_dataset_rows(data, datasets)

        return Response(data)


class RealWorldDatasets(APIView):
    """
    Request synthetic datasets
    """
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    renderer_classes = [JSONRenderer]

    def get(self, request):
        data = []

        datasets = DataSet.objects.filter(type=REAL_WORLD, is_training_data=False)
        data = datatable_dataset_rows(data, datasets)

        return Response(data)