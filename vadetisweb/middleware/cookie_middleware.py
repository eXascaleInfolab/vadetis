import logging

from vadetisweb.models import UserSetting
from vadetisweb.utils import settings_from_request_or_default_dict, update_setting_cookie
from vadetisweb.serializers import UserSettingSerializer

class UserCookieMiddleWare:
    """
    Middleware to set user setting cookie

    In case user is authenticated and has no setting cookie, set the cookie
    If the user is not authenticated and has no setting cookie, set the cookie
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Code to be executed for each request before the view (and later middleware) are called.

        response = self.get_response(request)
        # Code to be executed for each request/response after the view is called.
        settings_from_request, missing_keys = settings_from_request_or_default_dict(request)

        # authenticated user
        if request.user.is_authenticated:

            settings, created = UserSetting.objects.get_or_create(user=request.user)
            if created:
                # fill profile with values from cookies
                # (e.g. user used app, then later made an account -> values from cookies should be inserted into profile)
                for (key, value) in settings_from_request.items():
                    setattr(settings, key, value)
                settings.save()

            # update cookies based on stored values from setting model, we use our serializer for comfort
            serializer = UserSettingSerializer(instance=settings)
            update_setting_cookie(response, serializer.data, settings_from_request, missing_keys)

        elif not request.user.is_authenticated:  # anonymous user

            settings = UserSetting(**settings_from_request)
            serializer = UserSettingSerializer(instance=settings)
            update_setting_cookie(response, serializer.data, settings_from_request, missing_keys)

        return response
