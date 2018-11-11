# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from wipa2_show.models import *

# Register your models here.
class WorkPhotoInline(admin.TabularInline):
    model = WorkPhoto
    extra = 3

class DesignerInline(admin.TabularInline):
    model = Designer

class WorkAdmin(admin.ModelAdmin):
    inlines = [ WorkPhotoInline, DesignerInline ]

admin.site.register(Work, WorkAdmin)

