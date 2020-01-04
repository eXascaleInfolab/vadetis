from django.forms.widgets import CheckboxInput, TextInput
from django.utils.safestring import mark_safe

class IconCheckboxInput(CheckboxInput):
    def __init__(self, default=False, *args, **kwargs):
        super(IconCheckboxInput, self).__init__(*args, **kwargs)
        self.default = default

    def value_from_datadict(self, data, files, name):
        if name not in data:
            return self.default
        return super(IconCheckboxInput, self).value_from_datadict(data, files, name)

    def render(self, name, value, attrs=None, renderer=None):
        final_attrs = self.build_attrs(self.attrs, attrs)
        output = '<label class="mt-checkbox mt-checkbox-outline">'
        output += super(IconCheckboxInput, self).render(name, value, final_attrs, renderer)
        output += '<span></span></label>'
        return mark_safe(output)


class IconUserTextInput(TextInput):

    def __init__(self, type, *args, **kwargs):
        super(IconUserTextInput, self).__init__(*args, **kwargs)
        self.type = type
        self.attrs.update({
            'class': 'form-control form-control-solid placeholder-no-fix'
        })

    def render(self, name, value, attrs=None, renderer=None):
        final_attrs = self.build_attrs(self.attrs, attrs)
        if self.type == 'username' or self.type == 'username_email':
            output = '<div class="input-group"><span class="input-group-addon"><i class="fa fa-user"></i></span>'
        else:
            assert self.type == 'email'
            output = '<div class="input-group"><span class="input-group-addon"><i class="fa fa-envelope"></i></span>'

        output += super(IconUserTextInput, self).render(name, value, final_attrs, renderer)
        output += '</div>'
        return mark_safe(output)