from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer
from rest_framework_csv.renderers import CSVStreamingRenderer
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework import filters
from wsgiref.util import FileWrapper

from drf_yasg.utils import swagger_auto_schema
from django.contrib import messages
from django.shortcuts import redirect
from django.http import HttpResponse
from django.db.models import Q

from vadetisweb.models import DataSet
from vadetisweb.utils import strToBool, get_settings, dataset_to_json, get_datasets_from_json, df_zscore, export_to_csv, export_to_json
from vadetisweb.serializers import DatasetExportSerializer, DatasetSearchSerializer
from vadetisweb.factory import dataset_not_found_msg


class DatasetJson(APIView):
    """
    Request an original dataset from database
    """
    renderer_classes = [JSONRenderer]

    def get(self, request, dataset_id):
        try:
            dataset = DataSet.objects.filter(Q(id=dataset_id),
                                             Q(public=True) | Q(owner=request.user)).first()
            if dataset is None:
                return Response({}, status=status.HTTP_400_BAD_REQUEST)

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
        except:
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
                                      Q(public=True) | Q(owner=self.request.user))