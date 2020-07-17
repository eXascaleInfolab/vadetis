import logging
from wsgiref.util import FileWrapper

from django.db.models import Q
from django.http import HttpResponse
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, generics, filters
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_csv.renderers import CSVStreamingRenderer

from vadetisweb.models import DataSet
from vadetisweb.serializers import DatasetExportSerializer, DatasetSearchSerializer
from vadetisweb.utils import get_settings, dataset_to_json, df_zscore, export_to_csv, export_to_json, get_locations_json
from vadetisweb.utils.request_utils import q_shared_or_user_is_owner


class DatasetJson(APIView):
    """
    Request an original dataset from database
    """
    renderer_classes = [JSONRenderer]

    def get(self, request, dataset_id):
        try:

            dataset = DataSet.objects.filter(Q(id=dataset_id),
                                             q_shared_or_user_is_owner(request)).first()
            if dataset is None:
                return Response({}, status=status.HTTP_400_BAD_REQUEST)

            settings = get_settings(request)

            # handle query params
            type = request.query_params.get('type', 'raw')

            df = dataset.dataframe
            df_class = dataset.dataframe_class

            # transform dataframe if required
            if type == 'zscore':
                df = df_zscore(df)  # transform raw data to z-score values

            data = {}
            data['series'] = dataset_to_json(dataset, df, df_class, settings, type)

            return Response(data)

        except Exception as e:
            logging.error(e)
            return Response({}, status=status.HTTP_400_BAD_REQUEST)


class DatasetFileDownload(APIView):
    """
    Provides a download of a posted dataset
    """
    renderer_classes = [JSONRenderer, CSVStreamingRenderer]

    @swagger_auto_schema(request_body=DatasetExportSerializer)
    def post(self, request, format=None):

        try:
            serializer = DatasetExportSerializer(data=request.data)

            if serializer.is_valid():
                dataset_series_json = serializer.validated_data['dataset_series_json']

                if request.accepted_renderer.format == 'json':  # requested format is json
                    export_file = export_to_json(dataset_series_json)
                    response = HttpResponse(FileWrapper(export_file), content_type='application/json',
                                            status=status.HTTP_201_CREATED)
                    response['Content-Disposition'] = 'attachment; filename="%s"' % "export.json"
                    return response

                elif request.accepted_renderer.format == 'csv':
                    export_file = export_to_csv(dataset_series_json)
                    response = HttpResponse(FileWrapper(export_file), content_type='text/csv',
                                            status=status.HTTP_201_CREATED)
                    response['Content-Disposition'] = 'attachment; filename="%s"' % "export.csv"
                    return response

                else:
                    return Response({}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logging.error(e)
            return Response({}, status=status.HTTP_400_BAD_REQUEST)


class DatasetSearchView(generics.ListAPIView):
    """
    API View to search for datasets
    """
    renderer_classes = [JSONRenderer]
    search_fields = ['title', 'owner__username', 'training_dataset__title']
    filter_backends = (filters.SearchFilter,)
    serializer_class = DatasetSearchSerializer

    def get_queryset(self):
        return DataSet.objects.filter(Q(training_data=False),
                                      q_shared_or_user_is_owner(self.request))


class DatasetLocationsJson(APIView):
    """
    Request the locations of a dataset
    """
    renderer_classes = [JSONRenderer]

    def get(self, request, dataset_id):
        try:

            dataset = DataSet.objects.filter(Q(id=dataset_id),
                                             q_shared_or_user_is_owner(request)).first()

            if dataset is None or not dataset.is_spatial():
                return Response({}, status=status.HTTP_400_BAD_REQUEST)

            time_series = dataset.timeseries_set.all()
            data = get_locations_json(time_series)
            return Response(data)

        except Exception as e:
            logging.error(e)
            return Response({}, status=status.HTTP_400_BAD_REQUEST)