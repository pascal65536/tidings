# -*- coding: utf-8 -*-
from django import template

register = template.Library()


@register.inclusion_tag('inc/divider.html')
def divider(text):
    return {
        'text': text
    }
