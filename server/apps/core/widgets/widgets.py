from django.utils.encoding import force_text
from django.utils.html import format_html 
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string
from django.forms.widgets import TextInput, Select

from django.forms.utils import flatatt

class TagInput(TextInput):
    template_name = '_widgets/_tag_input.html'

    def render(self, name, value, attrs=None):
        attrs['placeholder'] = 'Add tags'
        if 'class' in attrs:
            attrs['class'] += ' tag-input'
        else:
            attrs['class'] = 'tag-input '
        context = {
            'input': super(TagInput, self).render(name, value, attrs),
            'id': attrs['id'],
        }
        return mark_safe(render_to_string(self.template_name, context))

    def value_from_datadict(self, data, files, name):
        print(data.get(name))
        return super(TagInput, self).value_from_datadict(data, files, name)


class DataAttribSelect(Select):
    """
     an HTML select widget with data attributes on the options.
    """
    template_name = '_widgets/_data_attribute_select.html'

    def __init__(self, data_attribute=None, data_value=None, *args, **kwargs):
        super(DataAttribSelect, self).__init__(*args, **kwargs)
        self.data_attribute = data_attribute
        self.data_value = data_value

    def render(self, name, value, attrs=None):
        if value is None:
            value = ''
        final_attrs = self.build_attrs(attrs, name=name)
        output = [format_html('<select{}>', flatatt(final_attrs))]
        options = self.render_options([value])
        if options:
            output.append(options)
        output.append('</select>')
        return mark_safe('\n'.join(output)) 

    def render_option(self, selected_choices, option_value, option_label):
        if option_value is None:
            option_value = ''
        option_value = force_text(option_value)
        if option_value in selected_choices:
            selected_html = mark_safe(' selected="selected"')
            if not self.allow_multiple_selected:
                # Only allow for a single selection.
                selected_choices.remove(option_value)
        else:
            selected_html = ''
        if self.data_attribute and self.data_value:
            return format_html('<option data-{}={} value="{}"{}>{}</option>',
                    self.data_attribute, self.data_value,
                    option_value, selected_html, force_text(option_label))
        return format_html('<option value="{}"{}>{}</option>',
                option_value, selected_html, force_text(option_label))
    
    def render_options(self, selected_choices):
        selected_choices = set(force_text(v) for v in selected_choices)
        output = []
        print(self.choices)
        for option_value, option_label, data_value in self.choices:
            if isinstance(option_label, (list, tuple)):
                output.append(format_html('<optgroup label="{}">', force_text(option_value)))
                for option in option_label:
                    output.append(self.render_option(selected_choices, *option))
                output.append('</optgroup>')
            else:
                output.append(self.render_option(selected_choices, option_value, option_label))
        return '\n'.join(output)
