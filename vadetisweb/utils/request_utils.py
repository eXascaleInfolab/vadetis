from django.db.models import Q

from vadetisweb.models import UserSetting
from vadetisweb.parameters import *
from .helper_function_utils import *


def q_shared_or_user_is_owner(request):
    query = Q()
    if request.user.is_authenticated:
        query |= Q(shared=True)
        query |= Q(owner=request.user)
    else:
        query = Q(shared=True)
    return query


def q_related_shared_or_user_is_owner(request):
    query = Q()
    if request.user.is_authenticated:
        query |= Q(datasets__shared=True)
        query |= Q(datasets__owner=request.user)
    else:
        query = Q(datasets__shared=True)
    return query


def settings_from_request_or_default_dict(request):
    """
    Returns a dict of the cookie values relevant for the (account) settings, returns default values if cookie is not available
    :param request: the request of the view
    :return: a dict of setting cookie values
    """
    settings = {}
    missing_keys = []

    _get_str_setting_from_cookie(settings, missing_keys, request, 'color_outliers', DEFAULT_COLOR_OUTLIERS)
    _get_str_setting_from_cookie(settings, missing_keys, request, 'color_true_positive', DEFAULT_COLOR_TRUE_POSITIVES)
    _get_str_setting_from_cookie(settings, missing_keys, request, 'color_false_positive', DEFAULT_COLOR_FALSE_POSITIVES)
    _get_str_setting_from_cookie(settings, missing_keys, request, 'color_false_negative', DEFAULT_COLOR_FALSE_NEGATIVES)

    return settings, missing_keys


def _get_int_setting_from_cookie(settings, missing_keys, request, cookie_name, default_value):
    cookie_value = request.COOKIES.get(cookie_name)
    if cookie_value is None:
        settings[cookie_name] = default_value
        missing_keys.append(cookie_name)
    else:
        settings[cookie_name] = int(cookie_value)


def _get_str_setting_from_cookie(settings, missing_keys, request, cookie_name, default_value):
    cookie_value = request.COOKIES.get(cookie_name)
    if cookie_value is None:
        settings[cookie_name] = default_value
        missing_keys.append(cookie_name)
    else:
        settings[cookie_name] = cookie_value


def get_settings(request):
    user = request.user
    settings = dict(DEFAULT_SETTINGS)  # default settings
    if user.is_authenticated:  # use settings
        try:
            user_settings = UserSetting.objects.get(user_id=user.id)  # profile holds settings for GUI
            # update settings dict from user settings
            for key in settings.keys():
                settings[key] = getattr(user_settings, key)

        except UserSetting.DoesNotExist:
            logging.debug('User has no settings, fallback to cookies!')
            settings, _ = settings_from_request_or_default_dict(request)

    else:  # use cookies
        settings, _ = settings_from_request_or_default_dict(request)

    return settings


def update_setting_cookie(response, validated_data, previous_setting=None, missing_keys=None):
    """
    :param response: response object to set new cookie values
    :param validated_data: validated serializer data of account settings
    :param previous_setting: (optional) previous setting to update only changed values
    :param missing_keys: (optional) cookie keys that were not available from request
    :return: an updated response, that will set the cookies on the client side
    """
    for key in validated_data.keys():
        if previous_setting is None or previous_setting[key] != validated_data[key] or (missing_keys is not None and key in missing_keys):
            response.set_cookie(key=key, value=validated_data[key], samesite='Lax')
