from django.contrib import messages
from django.shortcuts import reverse
from drf_yasg.utils import swagger_auto_schema
from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView

from vadetisweb.anomaly_algorithms.recommendation import *
from vadetisweb.factory import *
from vadetisweb.serializers import RecommendationSerializer
from vadetisweb.serializers.detection_serializers import *
from vadetisweb.utils import get_default_configuration, q_shared_or_user_is_owner


class RecommendationView(APIView):
    """
    Request anomaly recommendation
    """
    renderer_classes = [JSONRenderer]

    @swagger_auto_schema(request_body=RecommendationSerializer)
    def post(self, request, dataset_id):

        dataset = DataSet.objects.filter(Q(id=dataset_id, training_data=False),
                                         q_shared_or_user_is_owner(request)).first()
        if dataset is None:
            messages.error(request, dataset_not_found_msg(dataset_id))
            response = Response({}, status=status.HTTP_404_NOT_FOUND)
            response['Location'] = reverse('vadetisweb:index')
            return response

        serializer = RecommendationSerializer(context={'dataset': dataset}, data=request.data)

        if serializer.is_valid():
            algorithms = serializer.validated_data['algorithm']
            maximize_score = serializer.validated_data['maximize_score']
            data = { 'recommendations' : [] }
            for algorithm in algorithms:
                default_configuration = get_default_configuration(algorithm, maximize_score, dataset)

                try:
                    if algorithm == LISA_PEARSON:
                        serializer = LisaPearsonSerializer(context={'dataset_selected': dataset_id, 'dataset_series_json_required' : False, 'request': request}, data=default_configuration)
                        if serializer.is_valid():
                            info = lisa_pearson_recommendation(dataset.dataframe, dataset.dataframe_class, serializer.validated_data)
                            data['recommendations'].append({ 'algorithm' : algorithm, 'info' : info , 'conf' : serializer.data})

                    elif algorithm == LISA_DTW_PEARSON:
                        serializer = LisaDtwPearsonSerializer(context={'dataset_selected': dataset_id, 'dataset_series_json_required' : False, 'request': request}, data=default_configuration)
                        if serializer.is_valid():
                            info = lisa_dtw_recommendation(dataset.dataframe, dataset.dataframe_class, serializer.validated_data)
                            data['recommendations'].append({ 'algorithm' : algorithm, 'info' : info , 'conf' : serializer.data})

                    elif algorithm == LISA_SPATIAL:
                        serializer = LisaGeoDistanceSerializer(context={'dataset_selected': dataset_id, 'dataset_series_json_required' : False, 'request': request}, data=default_configuration)
                        if serializer.is_valid():
                            info = lisa_geo_recommendation(dataset.dataframe, dataset.dataframe_class, serializer.validated_data)
                            data['recommendations'].append({ 'algorithm' : algorithm, 'info' : info , 'conf' : serializer.data})

                    elif algorithm == RPCA_HUBER_LOSS:
                        serializer = RPCAMEstimatorLossSerializer(context={'dataset_selected': dataset_id, 'dataset_series_json_required' : False, 'request': request}, data=default_configuration)
                        if serializer.is_valid():
                            info = rpca_recommendation(dataset.dataframe, dataset.dataframe_class, serializer.validated_data)
                            data['recommendations'].append({ 'algorithm' : algorithm, 'info' : info , 'conf' : serializer.data})

                    elif algorithm == HISTOGRAM:
                        serializer = HistogramSerializer(context={'dataset_selected': dataset_id, 'dataset_series_json_required' : False, 'request': request}, data=default_configuration)
                        if serializer.is_valid():
                            info = histogram_recommendation(dataset.dataframe, dataset.dataframe_class, serializer.validated_data)
                            data['recommendations'].append({ 'algorithm' : algorithm, 'info' : info , 'conf' : serializer.data})

                    elif algorithm == CLUSTER_GAUSSIAN_MIXTURE:
                        serializer = ClusterSerializer(context={'dataset_selected': dataset_id, 'dataset_series_json_required' : False, 'request': request}, data=default_configuration)
                        if serializer.is_valid():
                            info = cluster_recommendation(dataset.dataframe, dataset.dataframe_class, serializer.validated_data)
                            data['recommendations'].append({ 'algorithm' : algorithm, 'info' : info , 'conf' : serializer.data})

                    elif algorithm == SVM:
                        serializer = SVMSerializer(context={'dataset_selected': dataset_id, 'dataset_series_json_required' : False, 'request': request}, data=default_configuration)
                        if serializer.is_valid():
                            info = svm_recommendation(dataset.dataframe, dataset.dataframe_class, serializer.validated_data)
                            data['recommendations'].append({ 'algorithm' : algorithm, 'info' : info , 'conf' : serializer.data})

                    elif algorithm == ISOLATION_FOREST:
                        serializer = IsolationForestSerializer(context={'dataset_selected': dataset_id, 'dataset_series_json_required' : False, 'request': request}, data=default_configuration)
                        if serializer.is_valid():
                            info = isolation_forest_recommendation(dataset.dataframe, dataset.dataframe_class, serializer.validated_data)
                            data['recommendations'].append({ 'algorithm' : algorithm, 'info' : info , 'conf' : serializer.data})

                except Exception as e:
                    logging.error(e)
                    return Response({}, status=status.HTTP_400_BAD_REQUEST)

            return Response(data, status=status.HTTP_200_OK)

        else:
            json_messages = []
            json_message_utils.error(json_messages, 'Invalid request')
            return response_invalid_form(serializer, json_messages)