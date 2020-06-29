import logging
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.parsers import MultiPartParser
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from celery.utils import uuid

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from vadetisweb.models import UserTasks
from vadetisweb.utils import settings_from_request_or_default_dict, update_setting_cookie, write_to_tempfile
from vadetisweb.serializers.account_serializers import *
from vadetisweb.serializers.dataset.account_dataset_serializer import *
from vadetisweb.tasks import TaskImportData, TaskImportTrainingData
from vadetisweb.factory import *

# TODO deprecated
from vadetisweb.forms.account_forms import *


#########################################################
# Account Views
#########################################################

@login_required
def account(request):
    """
    View for account setting
    """
    user_serializer = AccountUserSerializer(instance=request.user)
    password_update_serializer = AccountPasswordSerializer()
    social_disconnect_serializer = AccountSocialDisconnectSerializer()
    delete_account_serializer = AccountDeleteSerializer(instance=request.user)

    return render(request, 'vadetisweb/account/account.html', {'user_serializer': user_serializer,
                                                               'password_update_serializer': password_update_serializer,
                                                               'social_disconnect_serializer': social_disconnect_serializer,
                                                               'delete_account_serializer': delete_account_serializer})


@login_required
def account_datasets(request):
    search_serializer = AccountDatasetSearchSerializer()
    return render(request, 'vadetisweb/account/datasets/account_datasets.html', {'search_serializer': search_serializer})


@login_required
def account_training_datasets(request):
    search_serializer = AccountTrainingDatasetSearchSerializer()
    return render(request, 'vadetisweb/account/training_datasets/account_training_datasets.html',
                  {'search_serializer': search_serializer})


class ApplicationSetting(APIView):
    """
    Request applications settings on GET, or save them on POST
    """
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    template_name = 'vadetisweb/account/application_setting.html'

    def get(self, request, format=None):
        user = request.user
        settings_dict, _ = settings_from_request_or_default_dict(request)

        if user.is_authenticated:  # use profile
            settings, created = UserSetting.objects.get_or_create(user=user)
            if created:
                # fill profile with values from cookies
                # (e.g. user used app, then later made an account -> values from cookies should be inserted into profile)
                for (key, value) in settings_dict.items():
                    setattr(settings, key, value)
                settings.save()
        else:  # use cookies
            settings = UserSetting(**settings_dict)

        serializer = UserSettingSerializer(instance=settings)
        return Response({'serializer': serializer}, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        user = request.user

        if user.is_authenticated:  # use profile
            settings, _ = UserSetting.objects.get_or_create(user=user)
            serializer = UserSettingSerializer(instance=settings, data=request.data)
        else:
            serializer = UserSettingSerializer(data=request.data)

        if serializer.is_valid():
            if user.is_authenticated:  # use profile
                serializer.save()

            if request.accepted_renderer.format == 'json':  # requested format is json
                json_messages = []
                json_message_utils.success(json_messages, 'Settings saved')
                response = Response({
                    'status': 'success',
                    'messages': MessageSerializer(json_messages, many=True).data,
                }, status=status.HTTP_200_OK)
                settings_from_request, missing_keys = settings_from_request_or_default_dict(request)
                update_setting_cookie(response, serializer.validated_data, settings_from_request, missing_keys)

                return response

            else:  # or render html template
                messages.success(request, 'Settings saved')
                response = Response({
                    'serializer': serializer,
                }, status=status.HTTP_201_CREATED)
                settings_from_request, missing_keys = settings_from_request_or_default_dict(request)
                update_setting_cookie(response, serializer.validated_data, settings_from_request, missing_keys)
                return response

        else:  # invalid data provided
            message = "Form was invalid"
            if request.accepted_renderer.format == 'json':  # requested format is json
                json_messages = []
                json_message_utils.error(json_messages, message)
                return response_invalid_form(serializer, json_messages)

            else:  # or render html template
                messages.error(request, message)
                return Response({
                    'serializer': serializer,
                }, status=status.HTTP_400_BAD_REQUEST)


class AccountUploadDataset(APIView):
    """
    Upload a new dataset
    """
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    parser_classes = [MultiPartParser]
    template_name = 'vadetisweb/account/datasets/account_datasets_upload.html'

    def get(self, request, format=None):
        serializer = DatasetImportSerializer(context={"request": self.request, })
        return Response({'serializer': serializer}, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        user = request.user

        serializer = DatasetImportSerializer(context={"request": self.request, }, data=request.data)

        if serializer.is_valid():
            # handle dataset file
            dataset_file_raw = serializer.validated_data['csv_file']
            logging.info("Dataset file received: %s", dataset_file_raw.name)
            dataset_file = write_to_tempfile(dataset_file_raw)

            # handle spatial file
            spatial_file_raw = serializer.validated_data.get('csv_spatial_file', None)
            if spatial_file_raw is not None:
                logging.info("Spatial file received: %s", spatial_file_raw.name)
                spatial_file = write_to_tempfile(spatial_file_raw)
            else:
                spatial_file = None

            title = serializer.validated_data['title']
            type = serializer.validated_data['type']  # real world or synthetic

            # start import task
            user_tasks, _ = UserTasks.objects.get_or_create(user=user)
            task_uuid = uuid()
            if spatial_file is not None:
                user_tasks.apply_async(TaskImportData, args=[user.username, dataset_file.name, title, type],
                                       kwargs={'spatial_file_name': spatial_file.name},
                                       task_id=task_uuid)
            else:
                user_tasks.apply_async(TaskImportData, args=[user.username, dataset_file.name, title, type],
                                       task_id=task_uuid)

            message = "Importing Dataset Task (%s) created" % task_uuid

            if request.accepted_renderer.format == 'json':  # requested format is json
                json_messages = []
                json_message_utils.success(json_messages, message)
                return Response({
                    'status': 'success',
                    'messages': MessageSerializer(json_messages, many=True).data,
                }, status=status.HTTP_201_CREATED)

            else:  # or render html template
                messages.success(request, message)
                return Response({
                    'serializer': serializer,
                }, status=status.HTTP_201_CREATED)
        else:
            message = "Form was invalid"
            if request.accepted_renderer.format == 'json':  # requested format is json
                json_messages = []
                json_message_utils.error(json_messages, message)
                return response_invalid_form(serializer, json_messages)

            else:  # or render html template
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
    template_name = 'vadetisweb/account/training_datasets/account_training_datasets_upload.html'

    def get(self, request, format=None):
        serializer = TrainingDatasetImportSerializer(context={"request": self.request, })
        return Response({'serializer': serializer}, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        user = request.user
        serializer = TrainingDatasetImportSerializer(context={"request": self.request, }, data=request.data)

        if serializer.is_valid():
            title = serializer.validated_data['title']
            owner = serializer.validated_data['main_dataset'].owner
            main_dataset = serializer.validated_data['main_dataset']
            training_dataset_file_raw = serializer.validated_data['csv_file']

            # check if user is ok
            if owner == request.user and main_dataset.owner == request.user:
                logging.info("Training dataset file received: %s", training_dataset_file_raw.name)
                training_dataset_file = write_to_tempfile(training_dataset_file_raw)

                user_tasks, _ = UserTasks.objects.get_or_create(user=user)

                # start import task
                task_uuid = uuid()
                user_tasks.apply_async(TaskImportTrainingData,
                                       args=[user.username, main_dataset.id, training_dataset_file.name,
                                             title], task_id=task_uuid)

                message = 'Importing Training Dataset: Task (%s) created' % task_uuid
                if request.accepted_renderer.format == 'json':  # requested format is json
                    json_messages = []
                    json_message_utils.success(json_messages, message)
                    return Response({
                        'status': 'success',
                        'messages': MessageSerializer(json_messages, many=True).data,
                    }, status=status.HTTP_201_CREATED)

                else:  # or render html template
                    messages.error(request, message)
                    return Response({
                        'serializer': serializer,
                    }, status=status.HTTP_201_CREATED)
        else:
            message = "Form was invalid"
            if request.accepted_renderer.format == 'json':  # requested format is json
                json_messages = []
                json_message_utils.error(json_messages, message)

                # append non field form errors to message errors
                return response_invalid_form(serializer, json_messages)

            else:  # or render html template
                messages.error(request, message)
                return Response({
                    'serializer': serializer,
                }, status=status.HTTP_400_BAD_REQUEST)


class AccountDatasetEdit(APIView):
    """
    View for dataset editing
    """
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'vadetisweb/account/datasets/account_dataset_edit.html'

    def get(self, request, dataset_id):
        try:
            dataset = DataSet.objects.get(id=dataset_id, training_data=False)

            if dataset.owner == request.user:
                dataset_edit_serializer = AccountDatasetUpdateSerializer(instance=dataset)
                dataset_delete_serializer = AccountDatasetDeleteSerializer()

                return Response({'dataset': dataset,
                                 'dataset_edit_serializer': dataset_edit_serializer,
                                 'dataset_delete_serializer': dataset_delete_serializer},
                                status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_403_FORBIDDEN)

        except DataSet.DoesNotExist:
            messages.error(request, dataset_not_found_msg(dataset_id))
            return redirect('vadetisweb:account_datasets')


class AccountTrainingDatasetEdit(APIView):
    """
    View for dataset editing
    """
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'vadetisweb/account/training_datasets/account_training_dataset_edit.html'

    def get(self, request, dataset_id):
        try:
            training_dataset = DataSet.objects.get(id=dataset_id, training_data=True)

            if training_dataset.owner == request.user:
                training_dataset_edit_serializer = AccountDatasetUpdateSerializer(instance=training_dataset)
                training_dataset_delete_serializer = AccountDatasetDeleteSerializer()

                return Response({'training_dataset': training_dataset,
                                 'training_dataset_edit_serializer': training_dataset_edit_serializer,
                                 'training_dataset_delete_serializer': training_dataset_delete_serializer},
                                status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_403_FORBIDDEN)

        except DataSet.DoesNotExist:
            messages.error(request, dataset_not_found_msg(dataset_id))
            return redirect('vadetisweb:account_training_datasets')


# TODO depreacted
@login_required
def deprecated_account(request):
    current_user = request.user

    form_password = None
    form_account_delete = None
    form_social_disconnect = None
    user_serializer = AccountUserSerializer()

    if request.method == 'POST':

        # check which form was submitted
        if 'submit-user' in request.POST:
            form_user = AccountUserForm(instance=current_user, data=request.POST)
            if form_user.is_valid():
                user = form_user.save()
                message = "Your account has been updated!"
                messages.success(request, message)
            else:
                logging.error(form_user.errors)

        elif 'submit-social-account-disconnect' in request.POST:
            form_social_disconnect = AccountSocialDisconnectForm(request=request, data=request.POST)
            if form_social_disconnect.is_valid():
                form_social_disconnect.save()
                messages.success(request, "Social account has been disconnected from your Vadetis account!")
                form_social_disconnect = AccountSocialDisconnectForm(request=request)
            else:
                message = "Could not disconnect social account!"
                messages.error(request, message)
                logging.error(form_social_disconnect.errors)

    """if form_user is None:
        form_user = AccountUserForm(instance=current_user)"""

    if form_password is None and not request.user.has_usable_password():
        form_password = AccountSetPasswordForm(user=current_user)

    if form_social_disconnect is None:
        form_social_disconnect = AccountSocialDisconnectForm(request=request)

    url_social_connect_success_redirect = reverse('vadetisweb:account')

    response = render(request, 'vadetisweb/account/account.html', {'user_serializer': user_serializer,
                                                                   'form_password': form_password,
                                                                   'form_social_disconnect': form_social_disconnect,
                                                                   'form_account_delete': form_account_delete,
                                                                   'url_social_connect_success_redirect': url_social_connect_success_redirect
                                                                   })
    return response
