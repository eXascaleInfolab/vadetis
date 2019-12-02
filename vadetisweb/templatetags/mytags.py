from __future__ import unicode_literals

import re, datetime, time
import kombu.five
from django import template
from django.urls import reverse, NoReverseMatch, resolve, Resolver404
from django.utils.html import escape
from django.utils.encoding import smart_text
from django.utils.safestring import mark_safe
from django.conf import settings
from django.db.models import Model
from inspect import ismethod
from django.utils.six import wraps
from django.utils.translation import ugettext as _
#from lisa.utils import decompress_window_size TODO

register = template.Library()

CONTEXT_KEY = 'DJANGO_BREADCRUMB_LINKS'

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


def requires_request(func):
    @wraps(func)
    def wrapped(context, *args, **kwargs):
        if 'request' in context:
            return func(context, *args, **kwargs)

        return ''
    return wrapped


@register.simple_tag(takes_context=False)
def date_range(lower_date, higher_date):
    return higher_date - lower_date


@register.filter(name='addcss')
def addcss(field, css):
   return field.as_widget(attrs={"class":css})


@requires_request
def append_breadcrumb(context, label, viewname, args, kwargs):
    context['request'].META[CONTEXT_KEY] = context['request'].META.get(CONTEXT_KEY, []) + [(label, viewname, args, kwargs)]


@register.simple_tag(takes_context=True)
def breadcrumb(context, label, viewname, *args, **kwargs):
    append_breadcrumb(context, _(escape(label)), viewname, args, kwargs)
    return ''

"""
# Similar to breadcrumb but label is not escaped
@register.simple_tag(takes_context=True)
def breadcrumb_safe(context, label, viewname, *args, **kwargs):
    append_breadcrumb(context, _(label), viewname, args, kwargs)
    return ''


# Same as breadcrumb but label is not translated.
@register.simple_tag(takes_context=True)
def breadcrumb_raw(context, label, viewname, *args, **kwargs):
    append_breadcrumb(context, escape(label), viewname, args, kwargs)
    return ''


# Same as breadcrumb but label is not escaped and translated.
@register.simple_tag(takes_context=True)
def breadcrumb_raw_safe(context, label, viewname, *args, **kwargs):
    append_breadcrumb(context, label, viewname, args, kwargs)
    return ''
"""

# Render breadcrumbs html using css classes
@register.simple_tag(takes_context=True)
@requires_request
def render_breadcrumbs(context, *args):
    try:
        template_path = args[0]
    except IndexError:
        template_path = getattr(settings, 'BREADCRUMBS_TEMPLATE', 'vadetisweb/parts/breadcrumbs.html')

    links = []
    for (label, viewname, view_args, view_kwargs) in context['request'].META.get(CONTEXT_KEY, []):
        if isinstance(viewname, Model) and hasattr(viewname, 'get_absolute_url') and ismethod(viewname.get_absolute_url):
            url = viewname.get_absolute_url(*view_args, **view_kwargs)
        else:
            try:
                try:
                    current_app = context['request'].resolver_match.namespace
                except AttributeError:
                    try:
                        resolver_match = resolve(context['request'].path)
                        current_app = resolver_match.namespace
                    except Resolver404:
                        current_app = None
                url = reverse(viewname=viewname, args=view_args, kwargs=view_kwargs, current_app=current_app)
            except NoReverseMatch:
                url = viewname
        links.append((url, smart_text(label) if label else label))

    if not links:
        return ''

    context = context.flatten()

    context['breadcrumbs'] = links
    context['breadcrumbs_total'] = len(links)

    return mark_safe(template.loader.render_to_string(template_path, context).replace("\n", ""))


class BreadcrumbNode(template.Node):

    def __init__(self, nodelist, viewname, args):
        self.nodelist = nodelist
        self.viewname = viewname
        self.args = list(args)
        self.kwargs = {}
        for arg in args:
            if '=' in arg:
                name = arg.split('=')[0]
                val = '='.join(arg.split('=')[1:])
                self.kwargs[name] = val
                self.args.remove(arg)

    def render(self, context):
        if 'request' not in context:
            return ''
        label = self.nodelist.render(context)
        try:
            viewname = template.Variable(self.viewname).resolve(context)
        except template.VariableDoesNotExist:
            viewname = self.viewname
        args = self.parse_args(context)
        kwargs = self.parse_kwargs(context)
        append_breadcrumb(context, label, viewname, args, kwargs)
        return ''

    def parse_args(self, context):
        args = []
        for arg in self.args:
            try:
                value = template.Variable(arg).resolve(context)
            except template.VariableDoesNotExist:
                value = arg
            args.append(value)
        return args

    def parse_kwargs(self, context):
        kwargs = {}
        for name, val in self.kwargs.items():
            try:
                value = template.Variable(val).resolve(context)
            except template.VariableDoesNotExist:
                value = val
            kwargs[name] = value
        return kwargs


@register.tag
def breadcrumb_for(parser, token):
    bits = list(token.split_contents())
    end_tag = 'end' + bits[0]
    nodelist = parser.parse((end_tag,))
    parser.delete_first_token()
    return BreadcrumbNode(nodelist, bits[1], bits[2:])


# Removes all currently added breadcrumbs
@register.simple_tag(takes_context=True)
@requires_request
def clear_breadcrumbs(context, *args):
    context['request'].META.pop(CONTEXT_KEY, None)
    return ''


@register.filter(name='print_timestamp')
def print_timestamp(timestamp):
    try:
        #assume, that timestamp is given in seconds with decimal point
        ts = float(timestamp)
    except ValueError:
        return None
    return datetime.datetime.fromtimestamp(time.time() - (kombu.five.monotonic() - ts))
    #return time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(ts))
