from rest_framework import status
from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response

from django.urls import reverse

from vadetisweb.serializers import AlgorithmSerializer, HistogramSerializer, ClusterSerializer, SVMSerializer, IsolationForestSerializer
from vadetisweb.models import DataSet
from vadetisweb.parameters import LISA, HISTOGRAM, CLUSTER_GAUSSIAN_MIXTURE, SVM, ISOLATION_FOREST

class AnomalyDetectionFormView(APIView):
    """
    Request anomaly detection form
    """
    renderer_classes = [TemplateHTMLRenderer]
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
                else:
                    print('Form was not valid')

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
