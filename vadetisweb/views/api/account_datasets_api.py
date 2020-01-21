from rest_framework import status
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import redirect
from vadetisweb.models import DataSet
from vadetisweb.serializers import DatasetUploadSerializer, TrainingDatasetUploadSerializer, DatasetSerializer
from vadetisweb.utils import datatable_dataset_rows


class AccountDatasets(APIView):
    """
    Request information about datasets of current user
    """
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    renderer_classes = [JSONRenderer]

    def get(self, request):
        user = request.user
        data = []

        datasets = DataSet.objects.filter(owner=user, is_training_data=False)
        data = datatable_dataset_rows(data, datasets)

        return Response(data)


class AccountUploadDataset(APIView):
    """
    Upload a new dataset
    """
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'vadetisweb/account/account_datasets_upload.html'

    def get(self, request):
        serializer = DatasetUploadSerializer()
        return Response({'serializer': serializer}, status=status.HTTP_200_OK)

    def post(self, request):
        user = request.user

        return redirect('vadetisweb:account_datasets_upload')


class AccountTrainingDatasets(APIView):
    """
    Request information about datasets of current user
    """
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    renderer_classes = [JSONRenderer]

    def get(self, request):
        user = request.user
        data = []

        datasets = DataSet.objects.filter(owner=user, is_training_data=True)
        data = datatable_dataset_rows(data, datasets)

        return Response(data)


class AccountUploadTrainingDataset(APIView):
    """
    Upload a new dataset
    """
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'vadetisweb/account/account_training_datasets_upload.html'

    def get(self, request):
        serializer = TrainingDatasetUploadSerializer()
        return Response({'serializer': serializer}, status=status.HTTP_200_OK)

    def post(self, request):
        user = request.user

        return redirect('vadetisweb:account_trainig_datasets_upload')
