import urllib
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.response import Response

from django.shortcuts import redirect
from django.urls import reverse

from vadetisweb.serializers import AlgorithmSerializer, HistogramSerializer, ClusterSerializer, SVMSerializer, IsolationForestSerializer
from vadetisweb.models import DataSet
from vadetisweb.parameters import LISA, HISTOGRAM, CLUSTER_GAUSSIAN_MIXTURE, SVM, ISOLATION_FOREST, DIFFERENT_UNITS, PEARSON, DTW, GEO
from vadetisweb.utils import get_conf, get_settings, is_valid_conf, get_dataframes_for_ranges
from vadetisweb.algorithms import perform_lisa_person, perform_lisa_dtw, perform_lisa_geo, perform_histogram, perform_cluster, perform_svm, perform_isolation_forest

class AnomalyDetectionFormView(APIView):
    """
    Request anomaly detection form
    """
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    template_name = 'vadetisweb/parts/forms/anomaly_detection_serializer_form.html'

    def post(self, request, dataset_id):

        dataset = DataSet.objects.get(id=dataset_id)

        if 'algorithm' in request.POST:
            algorithm = request.POST['algorithm']
            if algorithm:

                if algorithm == LISA:
                    #form = formOutputForLISA(request)
                    print("LISA")

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


class DatasetPerformAnomalyDetectionJson(APIView):
    """
    Request anomaly detection dataset
    """
    renderer_classes = [JSONRenderer]

    def get(self, request, dataset_id):
        try:
            dataset = DataSet.objects.get(id=dataset_id)
            data = {}
            info = {}

            # todo
            perform_on_zscore = True if dataset.type_of_data == DIFFERENT_UNITS else False

            conf = get_conf(request)
            settings = get_settings(request)

            # abort condition
            if not is_valid_conf(conf):
                return Response({}, status=status.HTTP_400_BAD_REQUEST)

            df, df_class = get_dataframes_for_ranges(dataset, conf)

            if conf['algorithm'] == LISA:
                ts_selected_id = conf['ts_selected']
                if conf['correlation_algorithm'] == PEARSON:
                    data, info = perform_lisa_person(df, df_class, conf, ts_selected_id, dataset, settings)

                if conf['correlation_algorithm'] == DTW:
                    data, info = perform_lisa_dtw(df, df_class, conf, ts_selected_id, dataset, settings)

                if conf['correlation_algorithm'] == GEO:
                    data, info = perform_lisa_geo(df, df_class, conf, ts_selected_id, dataset, settings)


            elif conf['algorithm'] == HISTOGRAM:

                training_data_id = conf['td_selected']
                try:
                    training_dataset = DataSet.objects.get(id=training_data_id)
                    data, info = perform_histogram(df, df_class, conf, training_dataset, dataset, settings)

                except DataSet.DoesNotExist:
                    return Response({}, status=status.HTTP_400_BAD_REQUEST)


            elif conf['algorithm'] == CLUSTER_GAUSSIAN_MIXTURE:

                training_data_id = conf['td_selected']
                try:
                    training_dataset = DataSet.objects.get(id=training_data_id)
                    data, info = perform_cluster(df, df_class, conf, training_dataset, dataset, settings)

                except DataSet.DoesNotExist:
                    return Response({}, status=status.HTTP_400_BAD_REQUEST)


            elif conf['algorithm'] == SVM:

                training_data_id = conf['td_selected']
                try:
                    training_dataset = DataSet.objects.get(id=training_data_id)
                    data, info = perform_svm(df, df_class, conf, training_dataset, dataset, settings)
                except DataSet.DoesNotExist:
                    return Response({}, status=status.HTTP_400_BAD_REQUEST)


            elif conf['algorithm'] == ISOLATION_FOREST:

                training_data_id = conf['td_selected']
                try:
                    training_dataset = DataSet.objects.get(id=training_data_id)
                    data, info = perform_isolation_forest(df, df_class, conf, training_dataset, dataset, settings)
                except DataSet.DoesNotExist:
                    return Response({}, status=status.HTTP_400_BAD_REQUEST)

            return [data, info]

        except DataSet.DoesNotExist:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
