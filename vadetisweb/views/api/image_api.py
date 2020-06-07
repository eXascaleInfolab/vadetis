import logging, json, os
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from drf_yasg.utils import swagger_auto_schema
from wsgiref.util import FileWrapper
from django.http import HttpResponse
from django.core.files.temp import NamedTemporaryFile

from vadetisweb.utils.image_utils import *
from vadetisweb.serializers.image_serializers import *


class CnfImage(APIView):
    """
    Request cnf matrix
    """

    @swagger_auto_schema(request_body=CnfImageSerializer)
    def post(self, request):
        try:
            serializer = CnfImageSerializer(data=request.data)
            if serializer.is_valid():

                cnf_matrix = np.array(serializer.validated_data['cnf'])

                temp_image = NamedTemporaryFile(suffix='.png')
                plot_confusion_matrix(temp_image.name, cnf_matrix, classes=['Normal', 'Anomaly'], title='')
                file_size = os.path.getsize(temp_image.name)

                response = HttpResponse(FileWrapper(temp_image), content_type='image/png',
                                        status=status.HTTP_201_CREATED)
                response['Content-Disposition'] = 'attachment; filename="%s"' % "cnf.png"
                response['Content-Length'] = file_size
                return response
            else:
                return Response({}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)


class ThresholdsScoresImage(APIView):
    """
    Request threshold scores image
    """

    @swagger_auto_schema(request_body=ThresholdsScoresImageSerializer)
    def post(self, request):
        try:
            serializer = ThresholdsScoresImageSerializer(data=request.data)
            if serializer.is_valid():
                plot_data = serializer.validated_data['plot_data']
                thresholds = np.array(plot_data['thresholds'])
                scores = np.array(plot_data['threshold_scores'])

                temp_image = NamedTemporaryFile(suffix='.png')
                plot_thresholds_scores(temp_image.name, thresholds, scores)
                file_size= os.path.getsize(temp_image.name)

                response = HttpResponse(FileWrapper(temp_image), content_type='image/png',
                                        status=status.HTTP_201_CREATED)
                response['Content-Disposition'] = 'attachment; filename="%s"' % "threshold_scores.png"
                response['Content-Length'] = file_size

                return response
            else:
                return Response({}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)