from rest_framework import status
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.parsers import MultiPartParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.settings import api_settings
from drf_yasg.utils import swagger_auto_schema

from django.contrib import messages
from django.shortcuts import reverse
from django.db.models import Q

from vadetisweb.models import DataSet
from vadetisweb.serializers import SuggestionSerializer
from vadetisweb.serializers.detection_serializers import *
from vadetisweb.anomaly_algorithms import anomaly_injection
from vadetisweb.utils import get_default_configuration, q_public_or_user_is_owner
from vadetisweb.factory import *
from vadetisweb.parameters import *
from vadetisweb.anomaly_algorithms.suggestion import *


class SuggestionView(APIView):
    """
    Request anomaly suggestion
    """
    renderer_classes = [JSONRenderer]

    @swagger_auto_schema(request_body=SuggestionSerializer)
    def post(self, request, dataset_id):

        dataset = DataSet.objects.filter(Q(id=dataset_id, training_data=False),
                                         q_public_or_user_is_owner(request)).first()
        if dataset is None:
            messages.error(request, dataset_not_found_msg(dataset_id))
            response = Response({}, status=status.HTTP_404_NOT_FOUND)
            response['Location'] = reverse('vadetisweb:index')
            return response

        serializer = SuggestionSerializer(context={'dataset': dataset}, data=request.data)

        if serializer.is_valid():
            algorithm = serializer.validated_data['algorithm']
            data = {}
            default_configuration = get_default_configuration(algorithm, dataset)

            try:
                if algorithm == LISA_PEARSON:
                    serializer = LisaPearsonSerializer(context={'dataset_selected': dataset_id, 'dataset_series_json_required' : False, 'request': request}, data=default_configuration)
                    if serializer.is_valid():
                        info = lisa_pearson_suggestion(dataset.dataframe, dataset.dataframe_class, serializer.validated_data)
                        data['info'] = info
                    else:
                        return Response({}, status=status.HTTP_400_BAD_REQUEST)

                elif algorithm == LISA_DTW_PEARSON:
                    serializer = LisaDtwPearsonSerializer(context={'dataset_selected': dataset_id, 'dataset_series_json_required' : False, 'request': request}, data=default_configuration)
                    if serializer.is_valid():
                        info = lisa_dtw_suggestion(dataset.dataframe, dataset.dataframe_class, serializer.validated_data)
                        data['info'] = info
                    else:
                        return Response({}, status=status.HTTP_400_BAD_REQUEST)

                elif algorithm == LISA_SPATIAL:
                    serializer = LisaGeoDistanceSerializer(context={'dataset_selected': dataset_id, 'dataset_series_json_required' : False, 'request': request}, data=default_configuration)
                    if serializer.is_valid():
                        info = lisa_geo_suggestion(dataset.dataframe, dataset.dataframe_class, serializer.validated_data)
                        data['info'] = info
                    else:
                        return Response({}, status=status.HTTP_400_BAD_REQUEST)

                elif algorithm == RPCA_HUBER_LOSS:
                    serializer = RPCAMEstimatorLossSerializer(context={'dataset_selected': dataset_id, 'dataset_series_json_required' : False, 'request': request}, data=default_configuration)
                    if serializer.is_valid():
                        info = rpca_suggestion(dataset.dataframe, dataset.dataframe_class, serializer.validated_data)
                        data['info'] = info
                    else:
                        return Response({}, status=status.HTTP_400_BAD_REQUEST)

                elif algorithm == HISTOGRAM:
                    serializer = HistogramSerializer(context={'dataset_selected': dataset_id, 'dataset_series_json_required' : False, 'request': request}, data=default_configuration)
                    if serializer.is_valid():
                        info = histogram_suggestion(dataset.dataframe, dataset.dataframe_class, serializer.validated_data)
                        data['info'] = info
                    else:
                        return Response({}, status=status.HTTP_400_BAD_REQUEST)

                elif algorithm == CLUSTER_GAUSSIAN_MIXTURE:
                    serializer = ClusterSerializer(context={'dataset_selected': dataset_id, 'dataset_series_json_required' : False, 'request': request}, data=default_configuration)
                    if serializer.is_valid():
                        info = cluster_suggestion(dataset.dataframe, dataset.dataframe_class, serializer.validated_data)
                        data['info'] = info
                    else:
                        return Response({}, status=status.HTTP_400_BAD_REQUEST)

                elif algorithm == SVM:
                    serializer = SVMSerializer(context={'dataset_selected': dataset_id, 'dataset_series_json_required' : False, 'request': request}, data=default_configuration)
                    if serializer.is_valid():
                        info = svm_suggestion(dataset.dataframe, dataset.dataframe_class, serializer.validated_data)
                        data['info'] = info
                    else:
                        return Response({}, status=status.HTTP_400_BAD_REQUEST)

                elif algorithm == ISOLATION_FOREST:
                    serializer = IsolationForestSerializer(context={'dataset_selected': dataset_id, 'dataset_series_json_required' : False, 'request': request}, data=default_configuration)
                    if serializer.is_valid():
                        info = isolation_forest_suggestion(dataset.dataframe, dataset.dataframe_class, serializer.validated_data)
                        data['info'] = info
                    else:
                        return Response({}, status=status.HTTP_400_BAD_REQUEST)

                return Response(data, status=status.HTTP_200_OK)

            except Exception as e:
                logging.error(e)
                return Response({}, status=status.HTTP_400_BAD_REQUEST)

        else:
            json_messages = []
            json_message_utils.error(json_messages, 'Invalid request')
            return response_invalid_form(serializer, json_messages)