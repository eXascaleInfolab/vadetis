from __future__ import unicode_literals

import re, datetime, time
import kombu.five

from django.urls import reverse, NoReverseMatch, resolve
from django.utils.safestring import mark_safe
from django.template import Library
#from lisa.utils import decompress_window_size TODO

register = Library()

@register.simple_tag(takes_context=False)
def get_host_url(request):
    return request.build_absolute_uri("/").rstrip("/")


@register.simple_tag(takes_context=True)
def cookie(context, cookie_name):
    request = context['request']
    result = request.COOKIES.get(cookie_name, '')
    return result


@register.filter(takes_context=False)
def get_item(dict, key):
    return dict.get(key)


@register.filter
def number_of_dataset_values(dataset):
    return dataset.number_of_dataframe_values()


@register.filter
def number_of_dataset_normal_values(dataset):
    return dataset.number_of_normal_values()


@register.filter
def number_of_dataset_anomaly_values(dataset):
    return dataset.number_of_anomaly_values()


@register.filter
def count_number_of_training_datasets(dataset):
    return dataset.number_of_training_datasets()


@register.filter
def count_number_of_public_training_datasets(dataset):
    return dataset.number_of_training_datasets()


@register.simple_tag
def count_time_series_anomaly_values(dataset, ts_id):
    return dataset.number_of_time_series_anomaly_values(ts_id)


@register.filter(takes_context=False, is_safe=False, needs_autoescape=False)
def get_conf_item(dict, key):

    if key == 'algorithm':
        return mark_safe('Algorithm: %s<br />' % dict[key])

    if key == 'n_components':
        return mark_safe('Number of Components: %s<br />' % dict[key])

    if key == 'n_init':
        return mark_safe('Number of Inits: %s<br />' % dict[key])

    if key == 'gamma':
        return mark_safe('Gamma: %s<br />' % dict[key])

    if key == 'nu':
        return mark_safe('Nu: %s<br />' % dict[key])

    if key == 'bootstrap':
        return mark_safe('Bootstrap: %s<br />' % dict[key])

    if key == 'n_estimators':
        return mark_safe('Number of Estimators: %s<br />' % dict[key])

    if key == 'train_size':
        return mark_safe('Train Size: %s<br />' % dict[key])

    if key == 'random_seed':
        return mark_safe('Random Seed: %s<br />' % dict[key])

    if key == 'correlation_algorithm':
        return mark_safe('Correlation: %s<br />' % dict[key])

    """if key == 'window_size':
        window_size_list = decompress_window_size(dict[key], int_conversion=False)
        return mark_safe('Window Size: %s<br />' % " ".join(window_size_list))"""

    if key == 'min_periods':
        return mark_safe('Min Periods: %s<br />' % dict[key])

    if key == 'row_standardized':
        return mark_safe('Row Standardized: %s<br />' % dict[key])

    if key == 'dtw_distance_function':
        return mark_safe('DTW Distance Function: %s<br />' % dict[key])

    if key == 'geo_distance_function':
        return mark_safe('Geographic Distance Function: %s<br />' % dict[key])

    if key == 'lisa_outlier_threshold':
        return mark_safe('Outlier Threshold: %s<br />' % dict[key])

    if key == 'lisa_cluster_threshold':
        return mark_safe('Cluster Threshold: %s<br />' % dict[key])

    return ''


@register.simple_tag(takes_context=True)
def active_tree(context, pattern_or_urlname):
    try:
        pattern = '^' + reverse(pattern_or_urlname)
    except NoReverseMatch:
        pattern = pattern_or_urlname
    path = context['request'].path
    if re.search(pattern, path) and pattern != '^/':
        return 'active'
    if pattern == '^/' and path == '/':
        return 'active'
    return ''


@register.simple_tag(takes_context=True)
def active_tree_selected(context, pattern_or_urlname):
    try:
        pattern = '^' + reverse(pattern_or_urlname)
    except NoReverseMatch:
        pattern = pattern_or_urlname
    path = context['request'].path
    if re.search(pattern, path) and pattern != '^/':
        return '<span class="selected"></span>'
    if pattern == '^/' and path == '/':
        return '<span class="selected"></span>'
    return ''


@register.simple_tag(takes_context=True)
def active_tree_arrow_open(context, pattern_or_urlname):
    try:
        pattern = '^' + reverse(pattern_or_urlname)
    except NoReverseMatch:
        pattern = pattern_or_urlname
    path = context['request'].path
    if re.search(pattern, path) and pattern != '^/':
        return 'open'
    if pattern == '^/' and path == '/':
        return 'open'
    return ''


@register.simple_tag
def nav_active(request, url):
    """
    In template: {% nav_active request "url_name_here" %}
    """
    url_name = resolve(request.path).url_name
    if url_name == url:
        return "active"
    return ""


@register.simple_tag(takes_context=False)
def date_range(lower_date, higher_date):
    return higher_date - lower_date


@register.filter(name='addcss')
def addcss(field, css):
   return field.as_widget(attrs={"class":css})


@register.filter(name='print_timestamp')
def print_timestamp(timestamp):
    try:
        #assume, that timestamp is given in seconds with decimal point
        ts = float(timestamp)
    except ValueError:
        return None
    return datetime.datetime.fromtimestamp(time.time() - (kombu.five.monotonic() - ts))
    #return time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(ts))

