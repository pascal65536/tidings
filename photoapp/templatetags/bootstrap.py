# -*- coding: utf-8 -*-
#
from django import template
from django.template import Context
from django.template.loader import get_template
from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


def process_field(field, errors):
    if field.widget.is_hidden:
        return field
    if getattr(field.widget, 'input_type', None) == 'checkbox':
        el_css_class = 'form-check-input'
    elif field.widget.__class__.__name__.lower() == "textarea":
        el_css_class = 'form-control'
    else:
        el_css_class = 'form-control'
    old_class = field.widget.attrs.get('class', '').split(' ')

    if el_css_class not in old_class:
        old_class.append(el_css_class)
        if getattr(field, 'errors', None) or getattr(field, 'name', None) in errors:
            old_class.append('is-invalid')
    field.widget.attrs['class'] = ' '.join(old_class)
    return field


@register.filter
def bootstrap(element):
    element_type = element.__class__.__name__.lower()
    if element_type == 'boundfield':
        process_field(element.field, element.errors)
        # element.fields['name'].widget.attrs['class']
        template_ = get_template("bootstrapform/field.html")  # .render(ctx)
        context = {'field': element}
    else:
        has_management = getattr(element, 'management_form', None)
        if has_management:
            template_ = get_template("bootstrapform/formset.html")
            context = {'formset': element}
        else:
            for k, field in element.fields.items():
                process_field(field, element.errors)
            template_ = get_template("bootstrapform/form.html")
            context = {'form': element}

    return template_.render(context)


@register.filter
def bootstrap_range_fromset(element):
    has_management = getattr(element, 'management_form', None)
    if has_management:
        template = get_template("bootstrapform/formset_range_fromset.html")
        context = {'formset': element}
    else:
        template = get_template("bootstrapform/form_range_formset.html")
        context = {'form': element}

    return template.render(context)


@register.filter
def bs_inline(element):
    element_type = element.__class__.__name__.lower()

    if element_type == 'boundfield':
        template_ = get_template("bootstrapform/field-inline.html")
        context = {'field': element}
    else:
        has_management = getattr(element, 'management_form', None)
        if has_management:
            template_ = get_template("bootstrapform/formset-inline.html")
            context = {'formset': element}
        else:
            template_ = get_template("bootstrapform/form-inline.html")
            context = {'form': element}
    return template_.render(context)


@register.filter
def is_checkbox(field):
    return field.field.widget.__class__.__name__.lower() == "checkboxinput"


@register.filter
def is_multiple_checkbox(field):
    return field.field.widget.__class__.__name__.lower() == "checkboxselectmultiple"


@register.filter
def is_radio(field):
    return field.field.widget.__class__.__name__.lower() == "radioselect"


@register.filter
def is_hidden(field):
    return field.field.widget.__class__.__name__.lower() == "hiddeninput"


@register.filter
def is_textarea(field):
    return field.field.widget.__class__.__name__.lower() == "textarea"
