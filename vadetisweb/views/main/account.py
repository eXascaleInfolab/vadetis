from rest_framework import status
from django.shortcuts import redirect
from django.contrib import messages
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.settings import api_settings

from vadetisweb.models import UserSetting
from vadetisweb.utils import account_setting_cookie_dict, json_message_utils, update_setting_cookie
from vadetisweb.serializers import UserSettingSerializer, MessageSerializer


class ApplicationSetting(APIView):
    """
    Request applications settings on GET, or save them on POST
    """
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    template_name = 'vadetisweb/account/application_setting.html'

    def get(self, request, format=None):
        user = request.user
        settings_dict = account_setting_cookie_dict(request)

        if user.is_authenticated: # use profile
            settings, created = UserSetting.objects.get_or_create(user=user)
            if created:
                # fill profile with values from cookies
                # (e.g. user used app, then later made an account-> values from cookies should be inserted into profile)
                for (key, value) in settings_dict.items():
                    setattr(settings, key, value)
                settings.save()
        else: # use cookies
            settings = UserSetting(**settings_dict)

        serializer = UserSettingSerializer(instance=settings)
        return Response({'serializer': serializer}, status=status.HTTP_200_OK)


    def post(self, request, format=None):
        user = request.user

        if user.is_authenticated:  # use profile
            settings, _  = UserSetting.objects.get_or_create(user=user)
            serializer = UserSettingSerializer(instance=settings, data=request.data)
        else:
            serializer = UserSettingSerializer(data=request.data)

        if serializer.is_valid():
            if user.is_authenticated:  # use profile
                serializer.save()

            if request.accepted_renderer.format == 'json':  # requested format is json
                json_messages = []
                json_message_utils.success(json_messages, 'Setting saved')
                response = Response({
                    'status': 'success',
                    'messages': MessageSerializer(json_messages, many=True).data,
                }, status=status.HTTP_200_OK)
                update_setting_cookie(response, serializer.validated_data)
                return response

            else:  # or render html template
                messages.success(request, 'Setting saved')
                response = Response({
                    'serializer': serializer,
                }, status=status.HTTP_201_CREATED)
                update_setting_cookie(response, serializer.validated_data)
                return response

        else: # invalid data provided
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
                    'form_errors': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)

            else:  # or render html template
                messages.error(request, message)
                return Response({
                    'serializer': serializer,
                }, status=status.HTTP_400_BAD_REQUEST)