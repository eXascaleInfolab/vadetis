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
from vadetisweb.anomaly_algorithms.detection import *
from vadetisweb.factory import dataset_not_found_msg


class AnomalyDetectionAlgorithmSelectionView(APIView):
    """
    Request anomaly detection form based on selected algorithm
    """
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    template_name = 'vadetisweb/parts/forms/serializer_form.html'

    def post(self, request, dataset_id):
        dataset = DataSet.objects.filter(Q(id=dataset_id),
                                         q_public_or_user_is_owner(request)).first()
        if dataset is None:
            messages.error(request, dataset_not_found_msg(dataset_id))
            return redirect('vadetisweb:index')


        serializer = AlgorithmSerializer(data=request.data)
        if serializer.is_valid():
            algorithm = serializer.validated_data['algorithm']
            formid = 'anomaly_detection_form'

            if algorithm == LISA_PEARSON:
                return Response({
                    'dataset': dataset,
                    'formid': formid,
                    'url': reverse('vadetisweb:detection_lisa_person', args=[dataset_id]),
                    'class' : 'pt-0',
                    'serializer': LisaPearsonSerializer(context={'dataset_selected': dataset_id, 'request' : request }),
                    'submit_label': 'Run',
                }, status=status.HTTP_200_OK)

            elif algorithm == LISA_DTW_PEARSON:
                return Response({
                    'dataset': dataset,
                    'formid': formid,
                    'url': reverse('vadetisweb:detection_lisa_dtw_person', args=[dataset_id]),
                    'class': 'pt-0',
                    'serializer': LisaDtwPearsonSerializer(context={'dataset_selected': dataset_id, 'request' : request }),
                    'submit_label' : 'Run',
                }, status=status.HTTP_200_OK)

            elif algorithm == LISA_GEO:
                return Response({
                    'dataset': dataset,
                    'formid': formid,
                    'url': reverse('vadetisweb:detection_lisa_geo', args=[dataset_id]),
                    'class': 'pt-0',
                    'serializer': LisaGeoDistanceSerializer(context={'dataset_selected': dataset_id, 'request' : request }),
                    'submit_label' : 'Run',
                }, status=status.HTTP_200_OK)

            elif algorithm == RPCA_HUBER_LOSS:
                return Response({
                    'dataset': dataset,
                    'formid': formid,
                    'url': reverse('vadetisweb:detection_rpca_mestimator', args=[dataset_id]),
                    'class': 'pt-0',
                    'serializer': RPCAMEstimatorLossSerializer(context={'dataset_selected': dataset_id, 'request' : request }),
                    'submit_label' : 'Run',
                }, status=status.HTTP_200_OK)

            elif algorithm == HISTOGRAM:
                return Response({
                    'dataset': dataset,
                    'formid': formid,
                    'url': reverse('vadetisweb:detection_histogram', args=[dataset_id]),
                    'class': 'pt-0',
                    'serializer': HistogramSerializer(context={'dataset_selected': dataset_id, 'request' : request }),
                    'submit_label' : 'Run',
                }, status=status.HTTP_200_OK)

            elif algorithm == CLUSTER_GAUSSIAN_MIXTURE:
                return Response({
                    'dataset': dataset,
                    'formid': formid,
                    'url': reverse('vadetisweb:detection_cluster', args=[dataset_id]),
                    'class': 'pt-0',
                    'serializer': ClusterSerializer(context={'dataset_selected': dataset_id, 'request' : request }),
                    'submit_label': 'Run',
                }, status=status.HTTP_200_OK)

            elif algorithm == SVM:
                return Response({
                    'dataset': dataset,
                    'formid': formid,
                    'url': reverse('vadetisweb:detection_svm', args=[dataset_id]),
                    'class': 'pt-0',
                    'serializer': SVMSerializer(context={'dataset_selected': dataset_id, 'request' : request }),
                    'submit_label': 'Run',
                }, status=status.HTTP_200_OK)

            elif algorithm == ISOLATION_FOREST:
                return Response({
                    'dataset': dataset,
                    'formid': formid,
                    'url': reverse('vadetisweb:detection_isolation_forest', args=[dataset_id]),
                    'class': 'pt-0',
                    'serializer': IsolationForestSerializer(context={'dataset_selected': dataset_id, 'request' : request }),
                    'submit_label': 'Run',
                }, status=status.HTTP_200_OK)

            else:
                return Response(template_name='vadetisweb/parts/forms/empty.html', status=status.HTTP_204_NO_CONTENT)
        else:
            logging.error('Algorithm selection form was not valid')
            return Response(template_name='vadetisweb/parts/forms/empty.html', status = status.HTTP_204_NO_CONTENT)



class AnomalyDetectionLisaPearson(APIView):
    """
        Request anomaly detection from provided json
    """
    renderer_classes = [JSONRenderer]

    @swagger_auto_schema(request_body=LisaPearsonSerializer)
    def post(self, request, dataset_id):

        try:
            serializer = LisaPearsonSerializer(context={'dataset_selected': dataset_id, 'request' : request }, data=request.data)

            if serializer.is_valid():
                df_from_json, df_class_from_json = get_datasets_from_json(serializer.validated_data['dataset_series_json'])
                try:
                    data = {}
                    settings = get_settings(request)
                    data_series, info = lisa_pearson_from_validated_data(df_from_json, df_class_from_json, serializer.validated_data, settings)

                    data['series'] = data_series
                    data['info'] = info
                    return Response(data)

                except Exception as e:
                    logging.debug(e)
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
            serializer = LisaDtwPearsonSerializer(context={'dataset_selected': dataset_id, 'request' : request }, data=request.data)

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
            serializer = LisaGeoDistanceSerializer(context={'dataset_selected': dataset_id, 'request' : request }, data=request.data)

            if serializer.is_valid():
                df_from_json, df_class_from_json = get_datasets_from_json(serializer.validated_data['dataset_series_json'])
                try:
                    data = {}
                    """settings = get_settings(request)
                    data_series, info = histogram_from_validated_data(df_from_json, df_class_from_json, serializer.validated_data, settings)

                    data['series'] = data_series
                    data['info'] = info"""
                    return Response(data)

                except Exception as e:
                    logging.debug(e)
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
            serializer = RPCAMEstimatorLossSerializer(context={'dataset_selected': dataset_id, 'request' : request }, data=request.data)

            if serializer.is_valid():
                df_from_json, df_class_from_json = get_datasets_from_json(serializer.validated_data['dataset_series_json'])
                try:
                    data = {}
                    settings = get_settings(request)
                    data_series, info = rpca_from_validated_data(df_from_json, df_class_from_json, serializer.validated_data, settings)

                    data['series'] = data_series
                    data['info'] = info
                    return Response(data)

                except Exception as e:
                    logging.debug(e)
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
            serializer = HistogramSerializer(context={'dataset_selected': dataset_id, 'request' : request }, data=request.data)

            if serializer.is_valid():
                df_from_json, df_class_from_json = get_datasets_from_json(serializer.validated_data['dataset_series_json'])
                try:
                    data = {}
                    settings = get_settings(request)
                    data_series, info = histogram_from_validated_data(df_from_json, df_class_from_json, serializer.validated_data, settings)

                    data['series'] = data_series
                    data['info'] = info
                    return Response(data)

                except Exception as e:
                    logging.debug(e)
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
            serializer = ClusterSerializer(context={'dataset_selected': dataset_id, 'request' : request }, data=request.data)

            if serializer.is_valid():
                df_from_json, df_class_from_json = get_datasets_from_json(serializer.validated_data['dataset_series_json'])
                try:
                    data = {}
                    settings = get_settings(request)
                    data_series, info = cluster_from_validated_data(df_from_json, df_class_from_json, serializer.validated_data, settings)

                    data['series'] = data_series
                    data['info'] = info
                    return Response(data)

                except Exception as e:
                    logging.debug(e)
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
            serializer = SVMSerializer(context={'dataset_selected': dataset_id, 'request' : request }, data=request.data)

            if serializer.is_valid():
                df_from_json, df_class_from_json = get_datasets_from_json(serializer.validated_data['dataset_series_json'])
                try:
                    data = {}
                    settings = get_settings(request)
                    data_series, info = svm_from_validated_data(df_from_json, df_class_from_json, serializer.validated_data, settings)

                    data['series'] = data_series
                    data['info'] = info
                    return Response(data)


                except Exception as e:
                    logging.debug(e)
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
            serializer = IsolationForestSerializer(context={'dataset_selected': dataset_id, 'request' : request }, data=request.data)

            if serializer.is_valid():
                df_from_json, df_class_from_json = get_datasets_from_json(serializer.validated_data['dataset_series_json'])
                try:
                    data = {}
                    settings = get_settings(request)
                    data_series, info = isolation_forest_from_validated_data(df_from_json, df_class_from_json, serializer.validated_data, settings)

                    data['series'] = data_series
                    data['info'] = info
                    return Response(data)

                except Exception as e:
                    logging.debug(e)
                    return Response({}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({}, status=status.HTTP_400_BAD_REQUEST)

        except DataSet.DoesNotExist:
                messages.error(request, dataset_not_found_msg(dataset_id))
                return redirect('vadetisweb:index')


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


            except Exception as e:
                logging.debug(e)
                return Response({}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)

