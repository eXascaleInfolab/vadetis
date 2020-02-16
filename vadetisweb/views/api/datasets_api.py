from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from vadetisweb.models import DataSet
from vadetisweb.utils import datatable_dataset_rows, strToBool, get_settings, get_dataset_with_marker_json
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


class DatasetJson(APIView):
    """
    Request a dataset
    """
    renderer_classes = [JSONRenderer]

    def get(self, request, dataset_id):
        # handle query params
        type = request.GET.get('type', 'raw')
        show_anomalies = strToBool(request.query_params.get('show_anomalies', 'true'))

        data = {}
        settings = get_settings(request)
        dataset = DataSet.objects.get(id=dataset_id)

        data['series'] = get_dataset_with_marker_json(dataset, type, show_anomalies, settings)

        return Response(data)