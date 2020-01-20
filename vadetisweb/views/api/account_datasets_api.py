from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from vadetisweb.models import DataSet
from vadetisweb.utils import datatable_dataset_rows
from django.shortcuts import redirect

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
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'vadetisweb/account/account_datasets_upload.html'

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
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'vadetisweb/account/account_training_datasets_upload.html'

    def post(self, request):
        user = request.user

        return redirect('vadetisweb:account_trainig_datasets_upload')