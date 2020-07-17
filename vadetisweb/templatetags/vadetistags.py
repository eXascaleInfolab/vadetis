from __future__ import unicode_literals

import re, datetime, time

from django.urls import reverse, NoReverseMatch, resolve
from django.utils.safestring import mark_safe
from django.template import Library

register = Library()

@register.simple_tag(takes_context=False)
def get_host_url(request):
    return request.build_absolute_uri("/").rstrip("/")


@register.simple_tag(takes_context=True)
def cookie(context, cookie_name):
    request = context['request']
    result = request.COOKIES.get(cookie_name, '')
    return result


@register.filter
def human_readable_title(string):
    return re.sub(r"[^a-zA-Z0-9]+", ' ', string).title()


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
def contamination_level(dataset):
    return dataset.contamination_level()


@register.filter
def number_of_training_datasets(dataset):
    return dataset.number_of_training_datasets()


@register.filter
def number_of_shared_training_datasets(dataset):
    return dataset.number_of_shared_training_datasets()

@register.filter
def is_spatial(dataset):
    return dataset.is_spatial()


@register.simple_tag
def number_of_time_series_anomaly_values(dataset, ts_id):
    return dataset.number_of_time_series_anomaly_values(ts_id)

@register.simple_tag
def contamination_level_of_time_series(dataset, ts_id):
    return dataset.contamination_level_of_time_series(ts_id)

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

@register.filter()
def isoformat(dt):
    return dt.isoformat()

@register.filter
def get_type(value):
    return type(value)


