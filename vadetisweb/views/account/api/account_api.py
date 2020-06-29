from rest_framework import status
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from django.contrib import messages
from django.shortcuts import reverse
from django.contrib.auth import update_session_auth_hash

from vadetisweb.serializers import MessageSerializer
from vadetisweb.serializers.account_serializers import *
from vadetisweb.utils import json_message_utils
from vadetisweb.factory import response_invalid_form

class AccountUserUpdate(APIView):
    """
    View for account setting update processing
    """
    renderer_classes = [JSONRenderer]
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication, BasicAuthentication]

    def post(self, request):
        user_serializer = AccountUserSerializer(instance=request.user, data=request.data)

        if user_serializer.is_valid():
            user_serializer.save()
            json_messages = []
            json_message_utils.success(json_messages, 'Account saved')
            return Response({
                'status': 'success',
                'messages': MessageSerializer(json_messages, many=True).data,
            }, status=status.HTTP_200_OK)
        else:
            json_messages = []
            json_message_utils.error(json_messages, 'Form was not valid')
            return response_invalid_form(user_serializer, json_messages)


class AccountPasswordUpdate(APIView):
    """
    View for account setting update processing
    """
    renderer_classes = [JSONRenderer]
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication, BasicAuthentication]

    def post(self, request):
        password_update_serializer = AccountPasswordSerializer(context={"request": self.request, }, data=request.data)

        if password_update_serializer.is_valid():
            password_update_serializer.save()
            update_session_auth_hash(request, request.user)

            json_messages = []
            json_message_utils.success(json_messages, 'Password changed')
            return Response({
                'status': 'success',
                'messages': MessageSerializer(json_messages, many=True).data,
            }, status=status.HTTP_200_OK)
        else:
            json_messages = []
            json_message_utils.error(json_messages, 'Form was not valid')
            return response_invalid_form(password_update_serializer, json_messages)


class AccountSocialDisconnectUpdate(APIView):
    """
    View for account social disconnect processing
    """
    renderer_classes = [JSONRenderer]
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication, BasicAuthentication]

    def post(self, request):
        social_disconnect_serializer = AccountSocialDisconnectSerializer(data=request.POST)

        if social_disconnect_serializer.is_valid():
            social_disconnect_serializer.save()

            messages.success(request, "Saved")
            response = Response({}, status=status.HTTP_200_OK)
            response['Location'] = reverse('vadetisweb:account')
            return response

        else:
            json_messages = []
            json_message_utils.error(json_messages, 'Form was not valid')
            return response_invalid_form(social_disconnect_serializer, json_messages)


class AccountDelete(APIView):
    """
    View for account delete processing
    """
    renderer_classes = [JSONRenderer]
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication, BasicAuthentication]

    def post(self, request):
        account_delete_serializer = AccountDeleteSerializer(instance=request.user, data=request.POST)

        if account_delete_serializer.is_valid():

            deactivate_user = account_delete_serializer.save()

            # check if user no longer active, then delete
            # remove this if you want only to deactivate
            if deactivate_user.is_active == False:
                deactivate_user.delete()

                messages.success(request, "Account has been removed")
                response = Response({}, status=status.HTTP_200_OK)
                response['Location'] = reverse('vadetisweb:account_logout')
                return response

            else:
                return Response(status=status.HTTP_200_OK)

        else:
            json_messages = []
            json_message_utils.error(json_messages, 'Form was not valid')
            return response_invalid_form(account_delete_serializer, json_messages)