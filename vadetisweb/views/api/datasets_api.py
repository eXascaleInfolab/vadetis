from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework import viewsets, status

from drf_yasg.utils import swagger_auto_schema
from django.contrib import messages
from django.shortcuts import redirect

from vadetisweb.models import DataSet
from vadetisweb.utils import strToBool, get_settings, dataset_to_json, get_datasets_from_json, df_zscore
from vadetisweb.parameters import REAL_WORLD, SYNTHETIC
from vadetisweb.serializers import DatasetDataTablesSerializer, DatasetUpdateSerializer
from vadetisweb.factory import dataset_not_found_msg


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
    Request an original dataset from database
    """
    renderer_classes = [JSONRenderer]

    def get(self, request, dataset_id):
        try:
            dataset = DataSet.objects.get(id=dataset_id)
            settings = get_settings(request)

            # handle query params
            type = request.query_params.get('type', 'raw')
            show_anomaly = strToBool(request.query_params.get('show_anomaly', 'true'))

            df = dataset.dataframe
            df_class = dataset.dataframe_class

            # transform dataframe if required
            if type == 'zscore':
                df = df_zscore(df)  # transform raw data to z-score values

            data = {}
            data['series'] = dataset_to_json(dataset, df, df_class, show_anomaly, settings, type)

            return Response(data)

        except:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)


class DatasetUpdateJson(APIView):
    """
    Request an updated dataset for type
    """
    renderer_classes = [JSONRenderer]

    @swagger_auto_schema(request_body=DatasetUpdateSerializer)
    def post(self, request, dataset_id):
        # handle query params
        type = request.query_params.get('type', 'raw')
        show_anomaly = strToBool(request.query_params.get('show_anomaly', 'true'))

        try:
            serializer = DatasetUpdateSerializer(context={'dataset_selected': dataset_id, }, data=request.data)

            if serializer.is_valid():
                df_from_json, df_class_from_json = get_datasets_from_json(serializer.validated_data['dataset_series_json'])
                try:
                    data = {}
                    settings = get_settings(request)
                    dataset = DataSet.objects.get(id=dataset_id)

                    data['series'] = dataset_to_json(dataset, df_from_json, df_class_from_json,
                                                     show_anomaly, settings, 'raw')

                    return Response(data)

                except:
                    return Response({}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({}, status=status.HTTP_400_BAD_REQUEST)

        except DataSet.DoesNotExist:
            messages.error(request, dataset_not_found_msg(dataset_id))
            return redirect('vadetisweb:index')
