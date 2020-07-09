import logging
from .helper_function_utils import *

from django.db.models import Q

from vadetisweb.models import UserSetting
from vadetisweb.parameters import *


def q_public_or_user_is_owner(request):
    query = Q()
    if request.user.is_authenticated:
        query |= Q(public=True)
        query |= Q(owner=request.user)
    else:
        query = Q(public=True)
    return query


def q_related_public_or_user_is_owner(request):
    query = Q()
    if request.user.is_authenticated:
        query |= Q(datasets__public=True)
        query |= Q(datasets__owner=request.user)
    else:
        query = Q(datasets__public=True)
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
    _get_str_setting_from_cookie(settings, missing_keys, request, 'color_clusters', DEFAULT_COLOR_CLUSTERS)
    _get_str_setting_from_cookie(settings, missing_keys, request, 'color_true_positive', DEFAULT_COLOR_TRUE_POSITIVES)
    _get_str_setting_from_cookie(settings, missing_keys, request, 'color_false_positive', DEFAULT_COLOR_FALSE_POSITIVES)
    _get_str_setting_from_cookie(settings, missing_keys, request, 'color_false_negative', DEFAULT_COLOR_FALSE_NEGATIVES)

    _get_int_setting_from_cookie(settings, missing_keys, request, 'round_digits', DEFAULT_ROUND_DIGITS)

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


"""def get_conf_from_query_params(request):
    conf = {}

    algorithm = request.GET.get('algorithm', None)

    conf['time_range'] = request.GET.get("time_range", None)
    conf['range_start'] = convertToInt(request.GET.get("range_start", None))
    conf['range_end'] = convertToInt(request.GET.get("range_end", None))
    conf['maximize_score'] = request.GET.get("maximize_score", None)

    if algorithm == LISA_PEARSON:

        correlation_algorithm = request.GET.get('correlation_algorithm', None)

        if correlation_algorithm == PEARSON:
            conf['algorithm'] = algorithm
            conf['correlation_algorithm'] = correlation_algorithm
            conf['time_series'] = convertToInt(request.GET.get("time_series", ''))

            conf['window_size'] = request.GET.get("window_size", None)
            conf['window_size_unit'] = request.GET.get("window_size_unit", None)

            conf['min_periods'] = replaceEmptyStrWithNone(request.GET.get("min_periods", None))
            conf['normalize'] = convertStrToBoolean(request.GET.get("normalize", 'False'))

        elif correlation_algorithm == DTW:
            conf['algorithm'] = algorithm
            conf['correlation_algorithm'] = correlation_algorithm
            conf['time_series'] = convertToInt(request.GET.get("time_series", ''))

            conf['window_size'] = request.GET.get("window_size", None)
            conf['window_size_unit'] = request.GET.get("window_size_unit", None)

            conf['dtw_distance_function'] = request.GET.get("dtw_distance_function", '')
            conf['normalize'] = convertStrToBoolean(request.GET.get("normalize", 'False'))

        elif correlation_algorithm == GEO:
            conf['algorithm'] = algorithm
            conf['correlation_algorithm'] = correlation_algorithm
            conf['time_series'] = convertToInt(request.GET.get("time_series", ''))
            conf['geo_distance_function'] = request.GET.get("geo_distance_function", '')
            conf['normalize'] = convertStrToBoolean(request.GET.get("normalize", 'False'))

    elif algorithm == HISTOGRAM:
        conf['algorithm'] = algorithm
        conf['training_dataset'] = convertToInt(request.GET.get("training_dataset", ''))
        conf['train_size'] = convertToFloat(request.GET.get("train_size", ''))
        conf['random_seed'] = convertToInt(request.GET.get("random_seed", ''))

    elif algorithm == CLUSTER_GAUSSIAN_MIXTURE:
        conf['algorithm'] = algorithm
        conf['training_dataset'] = convertToInt(request.GET.get("training_dataset", ''))
        conf['train_size'] = convertToFloat(request.GET.get("train_size", ''))
        conf['random_seed'] = convertToInt(request.GET.get("random_seed", ''))

        conf['n_components'] = convertToInt(request.GET.get("n_components", ''))
        conf['n_init'] = convertToInt(request.GET.get("n_init", ''))

    elif algorithm == SVM:
        conf['algorithm'] = algorithm
        conf['training_dataset'] = convertToInt(request.GET.get("training_dataset", ''))
        conf['train_size'] = convertToFloat(request.GET.get("train_size", ''))
        conf['random_seed'] = convertToInt(request.GET.get("random_seed", ''))
        conf['kernel'] = request.GET.get("kernel", None)

        conf['gamma'] = convertToFloat(request.GET.get("gamma", None))
        if conf['gamma'] == None:
            conf['gamma'] = 'auto'

        conf['nu'] = convertToFloat(request.GET.get("nu", None))
        if conf['nu'] == None:
            conf['nu'] = 0.5

    elif algorithm == ISOLATION_FOREST:
        conf['algorithm'] = algorithm
        conf['training_dataset'] = convertToInt(request.GET.get("training_dataset", ''))
        conf['train_size'] = convertToFloat(request.GET.get("train_size", ''))
        conf['random_seed'] = convertToInt(request.GET.get("random_seed", ''))

        conf['bootstrap'] = convertStrToBoolean(request.GET.get("bootstrap", 'False'))
        conf['n_estimators'] = convertToInt(request.GET.get("n_estimators", ''))

    return conf"""
