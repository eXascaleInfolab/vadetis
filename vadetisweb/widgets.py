from django.forms.widgets import CheckboxInput, TextInput
from django.utils.safestring import mark_safe


class FormCheckboxInput(CheckboxInput):

    def __init__(self, default=False, label=None, *args, **kwargs):
        super(FormCheckboxInput, self).__init__(*args, **kwargs)
        self.default = default
        self.label = label

    def value_from_datadict(self, data, files, name):
        if name not in data:
            return self.default
        return super(FormCheckboxInput, self).value_from_datadict(data, files, name)

    def render(self, name, value, attrs=None, renderer=None):
        final_attrs = self.build_attrs(self.attrs, attrs)
        output = '<label class="kt-checkbox">'
        output += super(FormCheckboxInput, self).render(name, value, final_attrs, renderer)
        output += self.label
        output += '<span></span></label>'
        return mark_safe(output)


class UserTextInput(TextInput):

    def __init__(self, type, *args, **kwargs):
        super(UserTextInput, self).__init__(*args, **kwargs)
        self.type = type
        self.attrs.update({
            'class': 'form-control'
        })

    def render(self, name, value, attrs=None, renderer=None):
        final_attrs = self.build_attrs(self.attrs, attrs)
        return super(UserTextInput, self).render(name, value, final_attrs, renderer)