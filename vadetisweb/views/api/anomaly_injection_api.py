from rest_framework import status
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.views import APIView
from rest_framework.response import Response

from django.urls import reverse

from vadetisweb.models import DataSet
from vadetisweb.serializers import AnomalyInjectionSerializer
from vadetisweb.algorithms import anomaly_injection


class AnomalyInjectionFormView(APIView):
    """
    Request anomaly injection form
    """
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    template_name = 'vadetisweb/parts/forms/anomaly_detection_serializer_form.html'

    def post(self, request, dataset_id):

        try:
            dataset = DataSet.objects.get(id=dataset_id)
            serializer = AnomalyInjectionSerializer(data=request.data)

            if serializer.is_valid():
                df_inject, df_inject_class = anomaly_injection(dataset, serializer.data)



            return Response({
                'dataset' : dataset,
                'formid' : 'anomaly_detection_form',
                'url' : reverse('vadetisweb:anomaly_injection_form', args=[dataset_id]),
                'serializer' : serializer,
                }, status=status.HTTP_200_OK)

        except DataSet.DoesNotExist:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
