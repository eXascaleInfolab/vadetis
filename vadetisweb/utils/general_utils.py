from vadetisweb.parameters import *
from vadetisweb.models import UserSettings

def get_cookie_settings_dict(request):
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


def strToBool(v):
    s = str(v).lower()
    if s in ('true', 'yes', '1'):
         return True
    elif s in ('false', 'no', '0'):
         return False
    else:
         raise ValueError


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