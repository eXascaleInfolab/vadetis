from vadetisweb.parameters import LISA, PEARSON, DTW, GEO, HISTOGRAM, CLUSTER_GAUSSIAN_MIXTURE, SVM, ISOLATION_FOREST
from .helper_function_utils import *

from vadetisweb.models import UserSettings
from vadetisweb.parameters import *


def get_cookie_settings_dict(request):
    """
    Returns a dict of the cookie values relevant for the settings (profile), returns default values if cookie is not available
    :param request: the request of the view
    :return: a dict of cookie values
    """
    settings_dict = {}

    settings_dict['highcharts_height'] = int(request.COOKIES.get('highcharts_height', DEFAULT_HIGHCHARTS_HEIGHT))
    settings_dict['legend_height'] = int(request.COOKIES.get('legend_height', DEFAULT_LEGEND_HEIGHT))
    settings_dict['color_outliers'] = request.COOKIES.get('color_outliers', DEFAULT_COLOR_OUTLIERS)
    settings_dict['color_clusters'] = request.COOKIES.get('color_clusters', DEFAULT_COLOR_CLUSTERS)
    settings_dict['color_true_positive'] = request.COOKIES.get('color_true_positive', DEFAULT_COLOR_TRUE_POSITIVES)
    settings_dict['color_false_positive'] = request.COOKIES.get('color_false_positive', DEFAULT_COLOR_FALSE_POSITIVES)
    settings_dict['color_false_negative'] = request.COOKIES.get('color_false_negative', DEFAULT_COLOR_FALSE_NEGATIVES)
    settings_dict['round_digits'] = int(request.COOKIES.get('round_digits', DEFAULT_ROUND_DIGITS))

    return settings_dict


def get_settings(request):
    user = request.user
    settings = dict(DEFAULT_SETTINGS) # default settings
    if user.is_authenticated: # use settings
        try:
            user_settings = UserSettings.objects.get(user_id=user.id)  # profile holds settings for GUI
            # update settings dict from user settings
            for key in settings.keys():
                settings[key] = getattr(user_settings, key)

        except UserSettings.DoesNotExist:
            print('User has no settings, fallback to cookies!')
            settings = get_cookie_settings_dict(request)

    else: # use cookies
        settings = get_cookie_settings_dict(request)

    return settings


def get_conf_from_query_params(request):
    conf = {}

    algorithm = request.GET.get('algorithm', None)

    conf['time_range'] = request.GET.get("time_range", None)
    conf['range_start'] = convertToInt(request.GET.get("range_start", None))
    conf['range_end'] = convertToInt(request.GET.get("range_end", None))
    conf['maximize_score'] = request.GET.get("maximize_score", None)

    if algorithm == LISA:

        correlation_algorithm = request.GET.get('correlation_algorithm', None)

        if correlation_algorithm == PEARSON:
            conf['algorithm'] = algorithm
            conf['correlation_algorithm'] = correlation_algorithm
            conf['ts_selected'] = convertToInt(request.GET.get("ts_selected", ''))

            conf['window_size_value'] = request.GET.get("window_size_value", None)
            conf['window_size_unit'] = request.GET.get("window_size_unit", None)

            conf['min_periods'] = replaceEmptyStrWithNone(request.GET.get("min_periods", None))
            conf['row_standardized'] = convertStrToBoolean(request.GET.get("row_standardized", 'False'))

        elif correlation_algorithm == DTW:
            conf['algorithm'] = algorithm
            conf['correlation_algorithm'] = correlation_algorithm
            conf['ts_selected'] = convertToInt(request.GET.get("ts_selected", ''))

            conf['window_size_value'] = request.GET.get("window_size_value", None)
            conf['window_size_unit'] = request.GET.get("window_size_unit", None)

            conf['dtw_distance_function'] = request.GET.get("dtw_distance_function", '')
            conf['row_standardized'] = convertStrToBoolean(request.GET.get("row_standardized", 'False'))

        elif correlation_algorithm == GEO:
            conf['algorithm'] = algorithm
            conf['correlation_algorithm'] = correlation_algorithm
            conf['ts_selected'] = convertToInt(request.GET.get("ts_selected", ''))
            conf['geo_distance_function'] = request.GET.get("geo_distance_function", '')
            conf['row_standardized'] = convertStrToBoolean(request.GET.get("row_standardized", 'False'))

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

    return conf
