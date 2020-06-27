from rest_framework import status, viewsets
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authentication import SessionAuthentication, BasicAuthentication

from drf_yasg.utils import swagger_auto_schema

from django.contrib import messages
from django.shortcuts import redirect

from vadetisweb.models import DataSet
from vadetisweb.utils import json_message_utils
from vadetisweb.serializers import MessageSerializer
from vadetisweb.serializers.dataset.account_dataset_serializer import *
from vadetisweb.factory.message_factory import *

class AccountDatasetDataTableViewSet(viewsets.ModelViewSet):
    """
    Request information about datasets of current user
    """
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    queryset = DataSet.objects.all()
    serializer_class = AccountDatasetDataTablesSerializer
    http_method_names = ['get', 'head'] # disable http put, delete etc. from ViewSet

    def get_queryset(self):
        queryset = self.queryset
        query_set = queryset.filter(owner=self.request.user, training_data=False)
        return query_set

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'list':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]


class AccountTrainingDatasetDataTableViewSet(viewsets.ModelViewSet):
    """
    Request information about datasets of current user
    """
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    queryset = DataSet.objects.all()
    serializer_class = AccountTrainingDatasetDataTablesSerializer
    http_method_names = ['get', 'head'] # disable http put, delete etc. from ViewSet

    def get_queryset(self):
        queryset = self.queryset
        query_set = queryset.filter(owner=self.request.user, training_data=True)
        return query_set

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'list':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]


class AccountDatasetUpdate(APIView):
    """
    View to update a dataset
    """
    renderer_classes = [JSONRenderer]
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication, BasicAuthentication]

    @swagger_auto_schema(request_body=AccountDatasetUpdateSerializer)
    def post(self, request, dataset_id):
        try:
            dataset = DataSet.objects.get(id=dataset_id, training_data=False)
            dataset_edit_serializer = AccountDatasetUpdateSerializer(instance=dataset, data=request.POST)

            if dataset_edit_serializer.is_valid():

                if dataset.owner == request.user:
                    dataset_edit_serializer.save()

                    messages.success(request, dataset_saved_msg(dataset_id))
                    return redirect('vadetisweb:account_datasets')

                else:
                    return Response(status=status.HTTP_403_FORBIDDEN)

            else:
                json_messages = []
                json_message_utils.error(json_messages, 'Form was not valid')
                return Response({
                    'messages': MessageSerializer(json_messages, many=True).data,
                    'form_errors': dataset_edit_serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)

        except DataSet.DoesNotExist:
            messages.error(request, dataset_not_found_msg(dataset_id))
            return redirect('vadetisweb:account_datasets')


class AccountDatasetDelete(APIView):
    """
    View to delete a dataset
    """
    renderer_classes = [JSONRenderer]
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication, BasicAuthentication]

    @swagger_auto_schema(request_body=AccountDatasetDeleteSerializer)
    def post(self, request, dataset_id):
        try:
            dataset = DataSet.objects.get(id=dataset_id, training_data=False)
            dataset_delete_serializer = AccountDatasetDeleteSerializer(data=request.POST)

            if dataset_delete_serializer.is_valid():
                if dataset_delete_serializer.validated_data['confirm'] is True:
                    if dataset.owner == request.user:
                        dataset_title = dataset.title
                        dataset.delete()
                        messages.success(request, dataset_removed_msg(dataset_title))
                        return redirect('vadetisweb:account_datasets')
                    else:
                        return Response(status=status.HTTP_403_FORBIDDEN)
                else:
                    messages.warning(request, 'Check "Confirm" if you want to delete this dataset')
                    return redirect('vadetisweb:account_dataset_edit', dataset_id=dataset_id)
            else:
                message = "Form was invalid"
                json_messages = []
                json_message_utils.error(json_messages, message)

                # append non field form errors to message errors
                if (api_settings.NON_FIELD_ERRORS_KEY in dataset_delete_serializer.errors):
                    for non_field_error in dataset_delete_serializer.errors[api_settings.NON_FIELD_ERRORS_KEY]:
                        json_message_utils.error(json_messages, non_field_error)
                return Response({
                    'messages': MessageSerializer(json_messages, many=True).data,
                    'form_errors': dataset_delete_serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)


        except DataSet.DoesNotExist:
            messages.error(request, dataset_not_found_msg(dataset_id))
            return redirect('vadetisweb:account_datasets')