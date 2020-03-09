import urllib, json, base64
import numpy as np
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.response import Response

from django.urls import reverse
from django.core.files.temp import NamedTemporaryFile
from django.http import HttpResponse

from vadetisweb.serializers import AlgorithmSerializer, HistogramSerializer, ClusterSerializer, SVMSerializer, IsolationForestSerializer
from vadetisweb.models import DataSet
from vadetisweb.parameters import LISA, HISTOGRAM, CLUSTER_GAUSSIAN_MIXTURE, SVM, ISOLATION_FOREST, PEARSON, DTW, GEO
from vadetisweb.utils import get_datasets_from_json, get_lisa_serializer, plot_thresholds_scores, plot_confusion_matrix, get_conf, get_settings, is_valid_conf, get_dataframes_for_ranges, get_updated_dataset_series_for_threshold_with_marker_json
from vadetisweb.algorithms import perform_lisa_person, perform_lisa_dtw, perform_lisa_geo, perform_histogram, perform_cluster, perform_svm, perform_isolation_forest


class AnomalyDetectionFormView(APIView):
    """
    Request anomaly detection form
    """
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    template_name = 'vadetisweb/parts/forms/anomaly_detection_serializer_form.html'


    def post(self, request, dataset_id):
        dataset = DataSet.objects.get(id=dataset_id)
        try:
            if 'algorithm' in request.POST:
                algorithm = request.POST['algorithm']
                if algorithm:

                    if algorithm == LISA:
                        serializer = get_lisa_serializer(request.data, context={'dataset_selected': dataset_id, })

                    elif algorithm == HISTOGRAM:
                        serializer = HistogramSerializer(data=request.data, context={'dataset_selected': dataset_id, })

                    elif algorithm == CLUSTER_GAUSSIAN_MIXTURE:
                        serializer = ClusterSerializer(data=request.data, context={'dataset_selected': dataset_id, })

                    elif algorithm == SVM:
                        serializer = SVMSerializer(data=request.data, context={'dataset_selected': dataset_id, })

                    elif algorithm == ISOLATION_FOREST:
                        serializer = IsolationForestSerializer(data=request.data, context={'dataset_selected': dataset_id, })

                    else:
                        serializer = AlgorithmSerializer()

                    # check if a valid form has been submitted
                    if serializer.is_valid():
                        print("form was valid")
                        print(serializer.data)
                        url = "%s?%s" % (reverse('vadetisweb:synthetic_dataset_perform', args=(dataset_id,)),
                                         urllib.parse.urlencode(serializer.data))
                        response = Response({'serializer': serializer, })
                        response['Location'] = url
                        return response

                    else:
                        print('Form was not valid')
                        print(serializer.errors)

                else:
                    serializer = AlgorithmSerializer()
            else:
                serializer = AlgorithmSerializer()

            return Response({
                'dataset' : dataset,
                'formid' : 'anomaly_detection_form',
                'url' : reverse('vadetisweb:anomaly_detection_form', args=[dataset_id]),
                'serializer' : serializer,
                }, status=status.HTTP_200_OK)

        except DataSet.DoesNotExist:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)


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

            conf = get_conf(request)
            settings = get_settings(request)

            # abort condition
            if not is_valid_conf(conf):
                return Response({}, status=status.HTTP_400_BAD_REQUEST)

            df, df_class = get_dataframes_for_ranges(df_from_json, df_class_from_json, conf)

            if conf['algorithm'] == LISA:
                ts_selected_id = conf['ts_selected']

                if conf['correlation_algorithm'] == PEARSON:
                    data_series, info = perform_lisa_person(df, df_class, conf, ts_selected_id, dataset, settings)

                if conf['correlation_algorithm'] == DTW:
                    data_series, info = perform_lisa_dtw(df, df_class, conf, ts_selected_id, dataset, settings)

                if conf['correlation_algorithm'] == GEO:
                    data_series, info = perform_lisa_geo(df, df_class, conf, ts_selected_id, dataset, settings)


            elif conf['algorithm'] == HISTOGRAM:

                training_data_id = conf['td_selected']
                try:
                    training_dataset = DataSet.objects.get(id=training_data_id)
                    data_series, info = perform_histogram(df, df_class, conf, training_dataset, dataset, settings)

                except DataSet.DoesNotExist:
                    return Response({}, status=status.HTTP_400_BAD_REQUEST)


            elif conf['algorithm'] == CLUSTER_GAUSSIAN_MIXTURE:

                training_data_id = conf['td_selected']
                try:
                    training_dataset = DataSet.objects.get(id=training_data_id)
                    data_series, info = perform_cluster(df, df_class, conf, training_dataset, dataset, settings)

                except DataSet.DoesNotExist:
                    return Response({}, status=status.HTTP_400_BAD_REQUEST)


            elif conf['algorithm'] == SVM:

                training_data_id = conf['td_selected']
                try:
                    training_dataset = DataSet.objects.get(id=training_data_id)
                    data_series, info = perform_svm(df, df_class, conf, training_dataset, dataset, settings)
                except DataSet.DoesNotExist:
                    return Response({}, status=status.HTTP_400_BAD_REQUEST)


            elif conf['algorithm'] == ISOLATION_FOREST:
                training_data_id = conf['td_selected']
                try:
                    training_dataset = DataSet.objects.get(id=training_data_id)
                    data_series, info = perform_isolation_forest(df, df_class, conf, training_dataset, dataset,
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

            conf = get_conf(request)
            settings = get_settings(request)

            # abort condition
            if not is_valid_conf(conf):
                return Response({}, status=status.HTTP_400_BAD_REQUEST)

            df, df_class = get_dataframes_for_ranges(dataset.dataframe, dataset.dataframe_class, conf)

            if conf['algorithm'] == LISA:
                ts_selected_id = conf['ts_selected']

                if conf['correlation_algorithm'] == PEARSON:
                    data_series, info = perform_lisa_person(df, df_class, conf, ts_selected_id, dataset, settings)

                if conf['correlation_algorithm'] == DTW:
                    data_series, info = perform_lisa_dtw(df, df_class, conf, ts_selected_id, dataset, settings)

                if conf['correlation_algorithm'] == GEO:
                    data_series, info = perform_lisa_geo(df, df_class, conf, ts_selected_id, dataset, settings)


            elif conf['algorithm'] == HISTOGRAM:

                training_data_id = conf['td_selected']
                try:
                    training_dataset = DataSet.objects.get(id=training_data_id)
                    data_series, info = perform_histogram(df, df_class, conf, training_dataset, dataset, settings)

                except DataSet.DoesNotExist:
                    return Response({}, status=status.HTTP_400_BAD_REQUEST)


            elif conf['algorithm'] == CLUSTER_GAUSSIAN_MIXTURE:

                training_data_id = conf['td_selected']
                try:
                    training_dataset = DataSet.objects.get(id=training_data_id)
                    data_series, info = perform_cluster(df, df_class, conf, training_dataset, dataset, settings)

                except DataSet.DoesNotExist:
                    return Response({}, status=status.HTTP_400_BAD_REQUEST)


            elif conf['algorithm'] == SVM:

                training_data_id = conf['td_selected']
                try:
                    training_dataset = DataSet.objects.get(id=training_data_id)
                    data_series, info = perform_svm(df, df_class, conf, training_dataset, dataset, settings)
                except DataSet.DoesNotExist:
                    return Response({}, status=status.HTTP_400_BAD_REQUEST)


            elif conf['algorithm'] == ISOLATION_FOREST:
                training_data_id = conf['td_selected']
                try:
                    training_dataset = DataSet.objects.get(id=training_data_id)
                    data_series, info = perform_isolation_forest(df, df_class, conf, training_dataset, dataset, settings)

                except DataSet.DoesNotExist:
                    return Response({}, status=status.HTTP_400_BAD_REQUEST)

            data['series'] = data_series
            data['info'] = info
            return Response(data)

        except DataSet.DoesNotExist:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)


class DatasetThresholdUpdateJson(APIView):
    """
    Request anomaly detection dataset with new threshold
    """
    renderer_classes = [JSONRenderer]

    def post(self, request):

        data = {}
        new_info = {}

        threshold_post = request.POST['threshold']
        dataset_series_json_post = request.POST['dataset_series_json']
        info_post = request.POST['info']
        algorithm_post = request.POST['algorithm']

        threshold_str = json.loads(threshold_post)
        algorithm = json.loads(algorithm_post)
        threshold = float(threshold_str)
        dataset_series = json.loads(dataset_series_json_post)
        info = json.loads(info_post)

        settings = get_settings(request)

        data_series, new_info = get_updated_dataset_series_for_threshold_with_marker_json(threshold, dataset_series, info, algorithm, settings)

        data['series'] = data_series
        data['info'] = new_info

        return Response(data)


class CnfImage(APIView):
    """
    Request cnf matrix
    """

    def post(self, request):
        data = request.POST['data']
        cnf_matrix = np.array(json.loads(data))

        temp_image = NamedTemporaryFile(suffix='.png')
        plot_confusion_matrix(temp_image.name, cnf_matrix, classes=['Normal', 'Anomaly'], title='')

        open_tempfile = open(temp_image.name, 'rb')
        cnf_matrix_base64 = base64.b64encode(open_tempfile.read())
        return HttpResponse(cnf_matrix_base64, content_type="image/png")


class ThresholdsScoresImage(APIView):
    """
    Request threshold scores image
    """

    def post(self, request):
        thresholds = request.POST['thresholds']
        thresholds = np.array(json.loads(thresholds))

        scores = request.POST['scores']
        scores = np.array(json.loads(scores))

        temp_image = NamedTemporaryFile(suffix='.png')
        plot_thresholds_scores(temp_image.name, thresholds, scores)

        open_tempfile = open(temp_image.name, 'rb')
        image_base64 = base64.b64encode(open_tempfile.read())
        return HttpResponse(image_base64, content_type="image/png")
