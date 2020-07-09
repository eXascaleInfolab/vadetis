from rest_framework import status, viewsets
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authentication import SessionAuthentication

from drf_yasg.utils import swagger_auto_schema

from django.contrib import messages
from django.shortcuts import redirect

from vadetisweb.models import DataSet
from vadetisweb.utils import json_message_utils
from vadetisweb.serializers import MessageSerializer
from vadetisweb.serializers.dataset.account_dataset_serializer import *
from vadetisweb.factory import *


class AccountDatasetDataTableViewSet(viewsets.ModelViewSet):
    """
    Request information about datasets of current user
    """
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication]
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
    authentication_classes = [SessionAuthentication]
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
    authentication_classes = [SessionAuthentication]

    @swagger_auto_schema(request_body=AccountDatasetUpdateSerializer)
    def post(self, request, dataset_id):
        try:
            dataset = DataSet.objects.get(id=dataset_id, owner=request.user, training_data=False)
            dataset_edit_serializer = AccountDatasetUpdateSerializer(instance=dataset, data=request.data)

            if dataset_edit_serializer.is_valid():
                dataset_edit_serializer.save()

                messages.success(request, dataset_saved_msg(dataset_id))
                response = Response({}, status=status.HTTP_200_OK)
                response['Location'] = reverse('vadetisweb:account_datasets')
                return response

            else:
                json_messages = []
                json_message_utils.error(json_messages, 'Form was not valid')
                return response_invalid_form(dataset_edit_serializer, json_messages)

        except DataSet.DoesNotExist:
            messages.error(request, dataset_not_found_msg(dataset_id))
            response = Response({}, status=status.HTTP_404_NOT_FOUND)
            response['Location'] = reverse('vadetisweb:account_datasets')
            return response


class AccountDatasetDelete(APIView):
    """
    View to delete a dataset
    """
    renderer_classes = [JSONRenderer]
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication]

    @swagger_auto_schema(request_body=AccountDatasetDeleteSerializer)
    def post(self, request, dataset_id):
        try:
            dataset = DataSet.objects.get(id=dataset_id, owner=request.user, training_data=False)
            dataset_delete_serializer = AccountDatasetDeleteSerializer(data=request.data)

            if dataset_delete_serializer.is_valid():
                if dataset_delete_serializer.validated_data['confirm'] is True:
                    dataset_title = dataset.title
                    dataset.delete()

                    messages.success(request, dataset_removed_msg(dataset_title))
                    response = Response({}, status=status.HTTP_200_OK)
                    response['Location'] = reverse('vadetisweb:account_datasets')
                    return response

                else:
                    message = 'Check "Confirm" if you want to delete this dataset'
                    json_messages = []
                    json_message_utils.warning(json_messages, message)
                    return response_invalid_form(dataset_delete_serializer, json_messages)
            else:
                json_messages = []
                json_message_utils.error(json_messages, 'Form was not valid')
                return response_invalid_form(dataset_delete_serializer, json_messages)

        except DataSet.DoesNotExist:
            messages.error(request, dataset_not_found_msg(dataset_id))
            response = Response({}, status=status.HTTP_404_NOT_FOUND)
            response['Location'] = reverse('vadetisweb:account_datasets')
            return response


class AccountTrainingDatasetUpdate(APIView):
    """
    View to update a dataset
    """
    renderer_classes = [JSONRenderer]
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication]

    @swagger_auto_schema(request_body=AccountDatasetUpdateSerializer)
    def post(self, request, dataset_id):
        try:
            training_dataset = DataSet.objects.get(id=dataset_id, owner=request.user, training_data=True)
            training_dataset_edit_serializer = AccountDatasetUpdateSerializer(instance=training_dataset, data=request.data)

            if training_dataset_edit_serializer.is_valid():
                training_dataset_edit_serializer.save()

                messages.success(request, dataset_saved_msg(dataset_id))
                response = Response({}, status=status.HTTP_200_OK)
                response['Location'] = reverse('vadetisweb:account_training_datasets')
                return response

            else:
                json_messages = []
                json_message_utils.error(json_messages, 'Form was not valid')
                return response_invalid_form(training_dataset_edit_serializer, json_messages)

        except DataSet.DoesNotExist:
            messages.error(request, dataset_not_found_msg(dataset_id))
            response = Response({}, status=status.HTTP_404_NOT_FOUND)
            response['Location'] = reverse('vadetisweb:account_training_datasets')
            return response


class AccountTrainingDatasetDelete(APIView):
    """
    View to delete a dataset
    """
    renderer_classes = [JSONRenderer]
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication]

    @swagger_auto_schema(request_body=AccountDatasetDeleteSerializer)
    def post(self, request, dataset_id):
        try:
            training_dataset = DataSet.objects.get(id=dataset_id, owner=request.user, training_data=True)
            training_dataset_delete_serializer = AccountDatasetDeleteSerializer(data=request.data)

            if training_dataset_delete_serializer.is_valid():
                if training_dataset_delete_serializer.validated_data['confirm'] is True:
                    dataset_title = training_dataset.title
                    training_dataset.delete()

                    messages.success(request, dataset_removed_msg(dataset_title))
                    response = Response({}, status=status.HTTP_200_OK)
                    response['Location'] = reverse('vadetisweb:account_training_datasets')
                    return response

                else:
                    message = 'Check "Confirm" if you want to delete this dataset'
                    json_messages = []
                    json_message_utils.warning(json_messages, message)
                    return response_invalid_form(training_dataset_delete_serializer, json_messages)
            else:
                json_messages = []
                json_message_utils.error(json_messages, 'Form was not valid')
                return response_invalid_form(training_dataset_delete_serializer, json_messages)

        except DataSet.DoesNotExist:
            messages.error(request, dataset_not_found_msg(dataset_id))
            response = Response({}, status=status.HTTP_404_NOT_FOUND)
            response['Location'] = reverse('vadetisweb:account_training_datasets')
            return response
