from rest_framework import status
from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema

from django.urls import reverse
from django.shortcuts import redirect
from django.contrib import messages

from vadetisweb.serializers.detection_serializers import *
from vadetisweb.models import DataSet
from vadetisweb.utils import *
from vadetisweb.algorithms import *
from vadetisweb.factory import dataset_not_found_msg


class AnomalyDetectionAlgorithmSelectionView(APIView):
    """
    Request anomaly detection form based on selected algorithm
    """
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    template_name = 'vadetisweb/parts/forms/serializer_form.html'

    def post(self, request, dataset_id):
        try:
            dataset = DataSet.objects.get(id=dataset_id)
            serializer = AlgorithmSerializer(data=request.data)
            if serializer.is_valid():
                algorithm = serializer.validated_data['algorithm']
                formid = 'anomaly_detection_form'

                if algorithm == LISA_PEARSON:
                    return Response({
                        'dataset': dataset,
                        'formid': formid,
                        'url': reverse('vadetisweb:detection_lisa_person', args=[dataset_id]),
                        'serializer': LisaPearsonSerializer(context={'dataset_selected': dataset_id, }),
                        'submit_label': 'Run',
                    }, status=status.HTTP_200_OK)

                elif algorithm == LISA_DTW_PEARSON:
                    return Response({
                        'dataset': dataset,
                        'formid': formid,
                        'url': reverse('vadetisweb:detection_lisa_dtw_person', args=[dataset_id]),
                        'serializer': LisaDtwPearsonSerializer(context={'dataset_selected': dataset_id, }),
                        'submit_label' : 'Run',
                    }, status=status.HTTP_200_OK)

                elif algorithm == LISA_GEO:
                    return Response({
                        'dataset': dataset,
                        'formid': formid,
                        'url': reverse('vadetisweb:detection_lisa_geo', args=[dataset_id]),
                        'serializer': LisaGeoDistanceSerializer(context={'dataset_selected': dataset_id, }),
                        'submit_label' : 'Run',
                    }, status=status.HTTP_200_OK)

                elif algorithm == RPCA_HUBER_LOSS:
                    return Response({
                        'dataset': dataset,
                        'formid': formid,
                        'url': reverse('vadetisweb:detection_rpca_mestimator', args=[dataset_id]),
                        'serializer': RPCAMEstimatorLossSerializer(context={'dataset_selected': dataset_id, }),
                        'submit_label' : 'Run',
                    }, status=status.HTTP_200_OK)

                elif algorithm == HISTOGRAM:
                    return Response({
                        'dataset': dataset,
                        'formid': formid,
                        'url': reverse('vadetisweb:detection_histogram', args=[dataset_id]),
                        'serializer': HistogramSerializer(context={'dataset_selected': dataset_id, }),
                        'submit_label' : 'Run',
                    }, status=status.HTTP_200_OK)

                elif algorithm == CLUSTER_GAUSSIAN_MIXTURE:
                    return Response({
                        'dataset': dataset,
                        'formid': formid,
                        'url': reverse('vadetisweb:detection_cluster', args=[dataset_id]),
                        'serializer': ClusterSerializer(context={'dataset_selected': dataset_id, }),
                        'submit_label': 'Run',
                    }, status=status.HTTP_200_OK)

                elif algorithm == SVM:
                    return Response({
                        'dataset': dataset,
                        'formid': formid,
                        'url': reverse('vadetisweb:detection_svm', args=[dataset_id]),
                        'serializer': SVMSerializer(context={'dataset_selected': dataset_id, }),
                        'submit_label': 'Run',
                    }, status=status.HTTP_200_OK)

                elif algorithm == ISOLATION_FOREST:
                    return Response({
                        'dataset': dataset,
                        'formid': formid,
                        'url': reverse('vadetisweb:detection_isolation_forest', args=[dataset_id]),
                        'serializer': IsolationForestSerializer(context={'dataset_selected': dataset_id, }),
                        'submit_label': 'Run',
                    }, status=status.HTTP_200_OK)

                else:
                    return Response(template_name='vadetisweb/parts/forms/empty.html', status=status.HTTP_204_NO_CONTENT)
            else:
                logging.error('Algorithm selection form was not valid')
                return Response(template_name='vadetisweb/parts/forms/empty.html', status = status.HTTP_204_NO_CONTENT)

        except DataSet.DoesNotExist:
            messages.error(request, dataset_not_found_msg(dataset_id))
            return redirect('vadetisweb:index')


class AnomalyDetectionLisaPearson(APIView):
    """
        Request anomaly detection from provided json
    """
    renderer_classes = [JSONRenderer]

    @swagger_auto_schema(request_body=LisaPearsonSerializer)
    def post(self, request, dataset_id):

        try:
            serializer = LisaPearsonSerializer(context={'dataset_selected': dataset_id, }, data=request.data)

            if serializer.is_valid():
                df_from_json, df_class_from_json = get_datasets_from_json(serializer.validated_data['dataset_series_json'])
                try:
                    data = {}
                    settings = get_settings(request)
                    data_series, info = lisa_pearson_from_validated_data(df_from_json, df_class_from_json, serializer.validated_data, settings)

                    data['series'] = data_series
                    data['info'] = info
                    return Response(data)

                except:
                    return Response({}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({}, status=status.HTTP_400_BAD_REQUEST)

        except DataSet.DoesNotExist:
                messages.error(request, dataset_not_found_msg(dataset_id))
                return redirect('vadetisweb:index')


class AnomalyDetectionLisaDtwPearson(APIView):
    """
        Request anomaly detection from provided json
    """
    renderer_classes = [JSONRenderer]

    @swagger_auto_schema(request_body=LisaDtwPearsonSerializer)
    def post(self, request, dataset_id):

        try:
            serializer = LisaDtwPearsonSerializer(context={'dataset_selected': dataset_id, }, data=request.data)

            if serializer.is_valid():
                df_from_json, df_class_from_json = get_datasets_from_json(serializer.validated_data['dataset_series_json'])
                try:
                    data = {}
                    """settings = get_settings(request)
                    data_series, info = histogram_from_validated_data(df_from_json, df_class_from_json, serializer.validated_data, settings)

                    data['series'] = data_series
                    data['info'] = info"""
                    return Response(data)

                except:
                    return Response({}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({}, status=status.HTTP_400_BAD_REQUEST)

        except DataSet.DoesNotExist:
                messages.error(request, dataset_not_found_msg(dataset_id))
                return redirect('vadetisweb:index')


class AnomalyDetectionLisaGeoDistance(APIView):
    """
        Request anomaly detection from provided json
    """
    renderer_classes = [JSONRenderer]

    @swagger_auto_schema(request_body=LisaGeoDistanceSerializer)
    def post(self, request, dataset_id):

        try:
            serializer = LisaGeoDistanceSerializer(context={'dataset_selected': dataset_id, }, data=request.data)

            if serializer.is_valid():
                df_from_json, df_class_from_json = get_datasets_from_json(serializer.validated_data['dataset_series_json'])
                try:
                    data = {}
                    """settings = get_settings(request)
                    data_series, info = histogram_from_validated_data(df_from_json, df_class_from_json, serializer.validated_data, settings)

                    data['series'] = data_series
                    data['info'] = info"""
                    return Response(data)

                except:
                    return Response({}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({}, status=status.HTTP_400_BAD_REQUEST)

        except DataSet.DoesNotExist:
                messages.error(request, dataset_not_found_msg(dataset_id))
                return redirect('vadetisweb:index')


class AnomalyDetectionRPCAMEstimatorLoss(APIView):
    """
        Request anomaly detection from provided json
    """
    renderer_classes = [JSONRenderer]

    @swagger_auto_schema(request_body=RPCAMEstimatorLossSerializer)
    def post(self, request, dataset_id):

        try:
            serializer = RPCAMEstimatorLossSerializer(context={'dataset_selected': dataset_id, }, data=request.data)

            if serializer.is_valid():
                df_from_json, df_class_from_json = get_datasets_from_json(serializer.validated_data['dataset_series_json'])
                try:
                    data = {}
                    settings = get_settings(request)
                    data_series, info = rpca_from_validated_data(df_from_json, df_class_from_json, serializer.validated_data, settings)

                    data['series'] = data_series
                    data['info'] = info
                    return Response(data)

                except:
                    return Response({}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({}, status=status.HTTP_400_BAD_REQUEST)

        except DataSet.DoesNotExist:
                messages.error(request, dataset_not_found_msg(dataset_id))
                return redirect('vadetisweb:index')


class AnomalyDetectionHistogram(APIView):
    """
        Request anomaly detection from provided json
    """
    renderer_classes = [JSONRenderer]

    @swagger_auto_schema(request_body=HistogramSerializer)
    def post(self, request, dataset_id):

        try:
            serializer = HistogramSerializer(context={'dataset_selected': dataset_id, }, data=request.data)

            if serializer.is_valid():
                df_from_json, df_class_from_json = get_datasets_from_json(serializer.validated_data['dataset_series_json'])
                try:
                    data = {}
                    settings = get_settings(request)
                    data_series, info = histogram_from_validated_data(df_from_json, df_class_from_json, serializer.validated_data, settings)

                    data['series'] = data_series
                    data['info'] = info
                    return Response(data)

                except:
                    return Response({}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({}, status=status.HTTP_400_BAD_REQUEST)

        except DataSet.DoesNotExist:
                messages.error(request, dataset_not_found_msg(dataset_id))
                return redirect('vadetisweb:index')


class AnomalyDetectionCluster(APIView):
    """
        Request anomaly detection from provided json
    """
    renderer_classes = [JSONRenderer]

    @swagger_auto_schema(request_body=ClusterSerializer)
    def post(self, request, dataset_id):

        try:
            serializer = ClusterSerializer(context={'dataset_selected': dataset_id, }, data=request.data)

            if serializer.is_valid():
                df_from_json, df_class_from_json = get_datasets_from_json(serializer.validated_data['dataset_series_json'])
                try:
                    data = {}
                    settings = get_settings(request)
                    data_series, info = cluster_from_validated_data(df_from_json, df_class_from_json, serializer.validated_data, settings)

                    data['series'] = data_series
                    data['info'] = info
                    return Response(data)

                except:
                    return Response({}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({}, status=status.HTTP_400_BAD_REQUEST)

        except DataSet.DoesNotExist:
                messages.error(request, dataset_not_found_msg(dataset_id))
                return redirect('vadetisweb:index')


class AnomalyDetectionSVM(APIView):
    """
        Request anomaly detection from provided json
    """
    renderer_classes = [JSONRenderer]

    @swagger_auto_schema(request_body=SVMSerializer)
    def post(self, request, dataset_id):

        try:
            serializer = SVMSerializer(context={'dataset_selected': dataset_id, }, data=request.data)

            if serializer.is_valid():
                df_from_json, df_class_from_json = get_datasets_from_json(serializer.validated_data['dataset_series_json'])
                try:
                    data = {}
                    settings = get_settings(request)
                    data_series, info = svm_from_validated_data(df_from_json, df_class_from_json, serializer.validated_data, settings)

                    data['series'] = data_series
                    data['info'] = info
                    return Response(data)

                except:
                    return Response({}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({}, status=status.HTTP_400_BAD_REQUEST)

        except DataSet.DoesNotExist:
                messages.error(request, dataset_not_found_msg(dataset_id))
                return redirect('vadetisweb:index')


class AnomalyDetectionIsolationForest(APIView):
    """
        Request anomaly detection from provided json
    """
    renderer_classes = [JSONRenderer]

    @swagger_auto_schema(request_body=IsolationForestSerializer)
    def post(self, request, dataset_id):

        try:
            serializer = IsolationForestSerializer(context={'dataset_selected': dataset_id, }, data=request.data)

            if serializer.is_valid():
                df_from_json, df_class_from_json = get_datasets_from_json(serializer.validated_data['dataset_series_json'])
                try:
                    data = {}
                    settings = get_settings(request)
                    data_series, info = isolation_forest_from_validated_data(df_from_json, df_class_from_json, serializer.validated_data, settings)

                    data['series'] = data_series
                    data['info'] = info
                    return Response(data)

                except:
                    return Response({}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({}, status=status.HTTP_400_BAD_REQUEST)

        except DataSet.DoesNotExist:
                messages.error(request, dataset_not_found_msg(dataset_id))
                return redirect('vadetisweb:index')


# TODO Deprecated
class DatasetJsonPerformAnomalyDetectionJson(APIView):
    """
        Request anomaly detection from provided json
    """
    renderer_classes = [JSONRenderer]

    def post(self, request, dataset_id):
        try:
            dataset = DataSet.objects.get(id=dataset_id)
            data = {}
            data_series = {}
            info = {}

            dataset_series_json_post = request.POST['dataset_series_json']
            dataset_series = json.loads(dataset_series_json_post)
            df_from_json, df_class_from_json = get_datasets_from_json(dataset_series)

            conf = get_conf_from_query_params(request)
            settings = get_settings(request)

            # abort condition
            if not is_valid_conf(conf):
                return Response({}, status=status.HTTP_400_BAD_REQUEST)

            df, df_class = get_dataframes_for_ranges(df_from_json, df_class_from_json, conf)

            if conf['algorithm'] == LISA_PEARSON:
                time_series_id = conf['time_series']

                if conf['correlation_algorithm'] == PEARSON:
                    data_series, info = perform_lisa_person(df, df_class, conf, time_series_id, dataset, settings)

                if conf['correlation_algorithm'] == DTW:
                    data_series, info = perform_lisa_dtw(df, df_class, conf, time_series_id, dataset, settings)

                if conf['correlation_algorithm'] == GEO:
                    data_series, info = perform_lisa_geo(df, df_class, conf, time_series_id, dataset, settings)


            elif conf['algorithm'] == HISTOGRAM:

                training_data_id = conf['training_dataset']
                try:
                    training_dataset = DataSet.objects.get(id=training_data_id)
                    data_series, info = histogram_from_url(df, df_class, conf, dataset, training_dataset, settings)

                except DataSet.DoesNotExist:
                    return Response({}, status=status.HTTP_400_BAD_REQUEST)


            elif conf['algorithm'] == CLUSTER_GAUSSIAN_MIXTURE:

                training_data_id = conf['training_dataset']
                try:
                    training_dataset = DataSet.objects.get(id=training_data_id)
                    data_series, info = cluster_from_url(df, df_class, conf, training_dataset, dataset, settings)

                except DataSet.DoesNotExist:
                    return Response({}, status=status.HTTP_400_BAD_REQUEST)


            elif conf['algorithm'] == SVM:

                training_data_id = conf['training_dataset']
                try:
                    training_dataset = DataSet.objects.get(id=training_data_id)
                    data_series, info = svm_from_url(df, df_class, conf, training_dataset, dataset, settings)
                except DataSet.DoesNotExist:
                    return Response({}, status=status.HTTP_400_BAD_REQUEST)


            elif conf['algorithm'] == ISOLATION_FOREST:
                training_data_id = conf['training_dataset']
                try:
                    training_dataset = DataSet.objects.get(id=training_data_id)
                    data_series, info = isolation_forest_from_url(df, df_class, conf, training_dataset, dataset,
                                                                  settings)

                except DataSet.DoesNotExist:
                    return Response({}, status=status.HTTP_400_BAD_REQUEST)

            data['series'] = data_series
            data['info'] = info
            return Response(data)

        except DataSet.DoesNotExist:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)


class DatasetPerformAnomalyDetectionJson(APIView):
    """
    Request anomaly detection dataset
    """
    renderer_classes = [JSONRenderer]

    def get(self, request, dataset_id):
        try:
            dataset = DataSet.objects.get(id=dataset_id)
            data = {}
            data_series = {}
            info = {}

            conf = get_conf_from_query_params(request)
            settings = get_settings(request)

            # abort condition
            if not is_valid_conf(conf):
                return Response({}, status=status.HTTP_400_BAD_REQUEST)

            df, df_class = get_dataframes_for_ranges(dataset.dataframe, dataset.dataframe_class, conf)

            if conf['algorithm'] == LISA_PEARSON:
                time_series_id = conf['time_series']

                if conf['correlation_algorithm'] == PEARSON:
                    data_series, info = perform_lisa_person(df, df_class, conf, time_series_id, dataset, settings)

                if conf['correlation_algorithm'] == DTW:
                    data_series, info = perform_lisa_dtw(df, df_class, conf, time_series_id, dataset, settings)

                if conf['correlation_algorithm'] == GEO:
                    data_series, info = perform_lisa_geo(df, df_class, conf, time_series_id, dataset, settings)


            elif conf['algorithm'] == HISTOGRAM:

                training_data_id = conf['training_dataset']
                try:
                    training_dataset = DataSet.objects.get(id=training_data_id)
                    data_series, info = histogram_from_url(df, df_class, conf, dataset, training_dataset, settings)

                except DataSet.DoesNotExist:
                    return Response({}, status=status.HTTP_400_BAD_REQUEST)


            elif conf['algorithm'] == CLUSTER_GAUSSIAN_MIXTURE:

                training_data_id = conf['training_dataset']
                try:
                    training_dataset = DataSet.objects.get(id=training_data_id)
                    data_series, info = cluster_from_url(df, df_class, conf, training_dataset, dataset, settings)

                except DataSet.DoesNotExist:
                    return Response({}, status=status.HTTP_400_BAD_REQUEST)


            elif conf['algorithm'] == SVM:

                training_data_id = conf['training_dataset']
                try:
                    training_dataset = DataSet.objects.get(id=training_data_id)
                    data_series, info = svm_from_url(df, df_class, conf, training_dataset, dataset, settings)
                except DataSet.DoesNotExist:
                    return Response({}, status=status.HTTP_400_BAD_REQUEST)


            elif conf['algorithm'] == ISOLATION_FOREST:
                training_data_id = conf['training_dataset']
                try:
                    training_dataset = DataSet.objects.get(id=training_data_id)
                    data_series, info = isolation_forest_from_url(df, df_class, conf, training_dataset, dataset, settings)

                except DataSet.DoesNotExist:
                    return Response({}, status=status.HTTP_400_BAD_REQUEST)

            data['series'] = data_series
            data['info'] = info
            return Response(data)

        except DataSet.DoesNotExist:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)


class DatasetThresholdUpdateJson(APIView):
    """
    Request threshold form or anomaly detection dataset with new threshold
    """
    renderer_classes = [JSONRenderer]

    @swagger_auto_schema(request_body=ThresholdSerializer)
    def post(self, request):

        serializer = ThresholdSerializer(data=request.data)

        if serializer.is_valid():
            try:
                data = {}
                settings = get_settings(request)

                data_series, info = get_updated_dataset_series_for_threshold_json(serializer.validated_data['dataset_series_json'], serializer.validated_data['threshold'], settings)
                data['series'] = data_series['series']
                data['info'] = info
                return Response(data)

            except:
                return Response({}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)

