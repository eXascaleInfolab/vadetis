from rest_framework import status
from vadetisweb.models import UserSettings
from vadetisweb.utils import get_cookie_settings_dict

from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.views import APIView
from rest_framework.response import Response
from vadetisweb.serializers import UserSettingsSerializer
from django.shortcuts import redirect


class ApplicationSettings(APIView):
    """
    Request applications settings on GET, or save them on POST
    """
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'vadetisweb/account/application_settings.html'

    def get(self, request):
        user = request.user
        settings_dict = get_cookie_settings_dict(request)

        if user.is_authenticated: # use profile
            settings, created = UserSettings.objects.get_or_create(user=user)
            if created:
                # fill profile with values from cookies
                # (e.g. user used app, then later made an account-> values from cookies should be inserted into profile)
                for (key, value) in settings_dict.items():
                    setattr(settings, key, value)
                settings.save()
        else: # use cookies
            settings = UserSettings(**settings_dict)

        serializer = UserSettingsSerializer(instance=settings)
        return Response({'serializer': serializer}, status=status.HTTP_200_OK)


    def post(self, request):
        user = request.user
        settings_dict = get_cookie_settings_dict(request)

        if user.is_authenticated:  # use profile
            settings, _  = UserSettings.objects.get_or_create(user=user)
            serializer = UserSettingsSerializer(instance=settings, data=request.data)
        else:
            serializer = UserSettingsSerializer(data=request.data)

        if serializer.is_valid():
            if user.is_authenticated:  # use profile
                serializer.save()

            response = Response({'serializer': serializer})
            # update cookies
            for key in settings_dict.keys():
                response.set_cookie(key=key, value=serializer.validated_data[key])

            return response

        return redirect('vadetisweb:application_settings')
