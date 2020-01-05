from django import template
from django.utils.html import escape
from django.utils.six import wraps
from django.conf import settings
from django.db.models import Model
from django.urls import reverse, NoReverseMatch, resolve, Resolver404
from inspect import ismethod
from django.utils.encoding import smart_text
from django.utils.safestring import mark_safe

register = template.Library()
CONTEXT_KEY = 'DJANGO_BREADCRUMB_LINKS'

def requires_request(func):
    @wraps(func)
    def wrapped(context, *args, **kwargs):
        if 'request' in context:
            return func(context, *args, **kwargs)

        return ''
    return wrapped

@requires_request
def append_breadcrumb(context, label, viewname, args, kwargs):
    context['request'].META[CONTEXT_KEY] = context['request'].META.get(CONTEXT_KEY, []) + [(label, viewname, args, kwargs)]


@register.simple_tag(takes_context=True)
def breadcrumb(context, label, viewname, *args, **kwargs):
    append_breadcrumb(context, escape(label), viewname, args, kwargs)
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