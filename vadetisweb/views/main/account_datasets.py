import logging
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.renderers import  TemplateHTMLRenderer, JSONRenderer
from rest_framework.parsers import MultiPartParser
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.settings import api_settings

from django.contrib import messages
from celery.utils import uuid

from vadetisweb.models import UserTasks
from vadetisweb.serializers import DatasetImportSerializer, TrainingDatasetImportSerializer, MessageSerializer
from vadetisweb.utils import write_to_tempfile, json_message_utils
from vadetisweb.tasks import TaskImportData, TaskImportTrainingData
from vadetisweb.parameters import SPATIAL


class AccountUploadDataset(APIView):
    """
    Upload a new dataset
    """
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    parser_classes = [MultiPartParser]
    template_name = 'vadetisweb/account/account_datasets_upload.html'

    def get(self, request, format=None):
        serializer = DatasetImportSerializer(context={"request": self.request, })
        return Response({'serializer': serializer}, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        user = request.user

        serializer = DatasetImportSerializer(data=request.data, context={"request": self.request, })

        if serializer.is_valid():
            # handle dataset file
            dataset_file_raw = serializer.validated_data['csv_file']
            logging.info("Dataset file received: ", dataset_file_raw.name)
            dataset_file = write_to_tempfile(dataset_file_raw)

            # handle spatial file
            spatial_data = serializer.validated_data['spatial_data']
            if spatial_data == SPATIAL:
                spatial_file_raw = serializer.validated_data['csv_spatial_file']
                logging.info("Spatial file received: ", spatial_file_raw.name)
                spatial_file = write_to_tempfile(spatial_file_raw)
            else:
                spatial_file = None

            title = serializer.validated_data['title']
            type = serializer.validated_data['type']  # real world or synthetic

            # start import task
            user_tasks, _ = UserTasks.objects.get_or_create(user=user)
            task_uuid = uuid()
            if spatial_data == SPATIAL:
                user_tasks.apply_async(TaskImportData, args=[user.username, dataset_file.name, title,
                                                             type, spatial_data],
                                       kwargs={'spatial_file_name': spatial_file.name}, task_id=task_uuid)
            else:
                user_tasks.apply_async(TaskImportData, args=[user.username, dataset_file.name, title,
                                                             type, spatial_data], task_id=task_uuid)

            message = "Importing Dataset Task (%s) created" % task_uuid

            if request.accepted_renderer.format == 'json':  # requested format is json
                json_messages = []
                json_message_utils.success(json_messages, message)
                return Response({
                    'status': 'success',
                    'messages':  MessageSerializer(json_messages, many=True).data,
                }, status=status.HTTP_201_CREATED)

            else: # or render html template
                messages.success(request, message)
                return Response({
                    'serializer' : serializer,
                }, status=status.HTTP_201_CREATED)
        else:
            message = "Form was invalid"
            if request.accepted_renderer.format == 'json':  # requested format is json
                json_messages = []
                json_message_utils.error(json_messages, message)

                # append non field form errors to message errors
                if(api_settings.NON_FIELD_ERRORS_KEY in serializer.errors):
                    for non_field_error in serializer.errors[api_settings.NON_FIELD_ERRORS_KEY]:
                        json_message_utils.error(json_messages, non_field_error)

                return Response({
                    'messages': MessageSerializer(json_messages, many=True).data,
                    'form_errors': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)

            else : # or render html template
                messages.error(request, message)
                return Response({
                    'serializer': serializer,
                }, status=status.HTTP_400_BAD_REQUEST)


class AccountUploadTrainingDataset(APIView):
    """
    Upload a new dataset
    """
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    parser_classes = [MultiPartParser]
    template_name = 'vadetisweb/account/account_training_datasets_upload.html'

    def get(self, request, format=None):
        serializer = TrainingDatasetImportSerializer(context={"request": self.request, })
        return Response({'serializer': serializer}, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        user = request.user
        serializer = TrainingDatasetImportSerializer(data=request.data, context={"request": self.request, })

        if serializer.is_valid():
            title = serializer.validated_data['title']
            owner = serializer.validated_data['original_dataset'].owner
            original_dataset = serializer.validated_data['original_dataset']
            training_dataset_file_raw = serializer.validated_data['csv_file']

            # check if user is ok
            if owner == request.user and original_dataset.owner == request.user:
                logging.info("Training dataset file received: ", training_dataset_file_raw.name)
                training_dataset_file = write_to_tempfile(training_dataset_file_raw)

                user_tasks, _ = UserTasks.objects.get_or_create(user=user)

                # start import task
                task_uuid = uuid()
                user_tasks.apply_async(TaskImportTrainingData,
                                       args=[user.username, original_dataset.id, training_dataset_file.name,
                                             title], task_id=task_uuid)

                message = 'Importing Training Dataset: Task (%s) created' % task_uuid
                if request.accepted_renderer.format == 'json':  # requested format is json
                    json_messages = []
                    json_message_utils.success(json_messages, message)
                    return Response({
                        'status': 'success',
                        'message': MessageSerializer(json_messages, many=True).data,
                    }, status=status.HTTP_201_CREATED)

                else:  # or render html template
                    messages.error(request, message)
                    return Response({
                        'serializer': serializer,
                    }, status=status.HTTP_201_CREATED)
            else:
                message = "Form was invalid"
        else:
            message = "Form was invalid"

        if request.accepted_renderer.format == 'json':  # requested format is json
            json_messages = []
            json_message_utils.error(json_messages, message)

            # append non field form errors to message errors
            if (api_settings.NON_FIELD_ERRORS_KEY in serializer.errors):
                for non_field_error in serializer.errors[api_settings.NON_FIELD_ERRORS_KEY]:
                    json_message_utils.error(json_messages, non_field_error)

            return Response({
                'messages': MessageSerializer(json_messages, many=True).data,
                'form_errors': serializer.errors,
            }, status=status.HTTP_400_BAD_REQUEST)

        else : # or render html template
            return Response({
                'serializer': serializer,
            }, status=status.HTTP_400_BAD_REQUEST)
