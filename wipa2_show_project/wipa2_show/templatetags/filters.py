# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from importlib import import_module

from django import template
from django import forms

register = template.Library()

@register.filter
def isinst(value, class_str):
    split = class_str.split('.')
    return isinstance(value, getattr(import_module('.'.join(split[:-1])), split[-1]))
