
from vadetisweb.parameters import *

def cookie_settings_dict(request):
    """
    Returns a dict of the cookie values relevant for the settings (profile), returns default values if cookie is not available
    :param request: the request of the view
    :return: a dict of cookie values
    """
    settings_dict = {}

    settings_dict['highcharts_height'] = int(request.COOKIES.get('highcharts_height', DEFAULT_HIGHCHARTS_HEIGHT ))
    settings_dict['legend_height'] = int(request.COOKIES.get('legend_height', DEFAULT_LEGEND_HEIGHT))
    settings_dict['color_outliers'] = request.COOKIES.get('color_outliers', DEFAULT_COLOR_OUTLIERS)
    settings_dict['color_clusters'] = request.COOKIES.get('color_clusters', DEFAULT_COLOR_CLUSTERS)
    settings_dict['color_true_positive'] = request.COOKIES.get('color_true_positive', DEFAULT_COLOR_TRUE_POSITIVES)
    settings_dict['color_false_positive'] = request.COOKIES.get('color_false_positive', DEFAULT_COLOR_FALSE_POSITIVES)
    settings_dict['color_false_negative'] = request.COOKIES.get('color_false_negative', DEFAULT_COLOR_FALSE_NEGATIVES)
    settings_dict['round_digits'] = int(request.COOKIES.get('round_digits', DEFAULT_ROUND_DIGITS))

    return settings_dict