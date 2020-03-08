from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAdminUser

from vadetisweb.models import DataSet
from vadetisweb.utils import strToBool, get_settings, get_dataset_with_marker_json
from vadetisweb.parameters import REAL_WORLD, SYNTHETIC
from vadetisweb.serializers import DatasetDataTablesSerializer


class SyntheticDatasetDataTableViewSet(viewsets.ModelViewSet):
    """
    Request synthetic datasets
    """
    queryset = DataSet.objects.all()
    serializer_class = DatasetDataTablesSerializer

    def get_queryset(self):
        queryset = self.queryset
        query_set = queryset.filter(type=SYNTHETIC, is_public=True, is_training_data=False)
        return query_set

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'list':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]


class RealWorldDatasetDataTableViewSet(viewsets.ModelViewSet):
    """
    Request real-world datasets
    """
    queryset = DataSet.objects.all()
    serializer_class = DatasetDataTablesSerializer

    def get_queryset(self):
        queryset = self.queryset
        query_set = queryset.filter(type=REAL_WORLD, is_public=True, is_training_data=False)
        return query_set

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'list':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]


class DatasetJson(APIView):
    """
    Request a dataset
    """
    renderer_classes = [JSONRenderer]

    def get(self, request, dataset_id):
        # handle query params
        type = request.query_params.get('type', 'raw')
        show_anomaly = strToBool(request.query_params.get('show_anomaly', 'true'))

        data = {}
        settings = get_settings(request)
        dataset = DataSet.objects.get(id=dataset_id)

        data['series'] = get_dataset_with_marker_json(dataset, dataset.dataframe, dataset.dataframe_class, type, show_anomaly, settings)

        return Response(data)
