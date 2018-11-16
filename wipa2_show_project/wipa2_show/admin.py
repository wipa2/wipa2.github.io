# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.contrib.admin import AdminSite
from django.contrib.admin import site
from django.urls import path
from django.views import generic

from wipa2_show.models import *


class WorksListView(generic.ListView):
    template_name = 'works_list.html'
    context_object_name = 'works_list'

    def get_queryset(self):
        return Work.objects.all()


class WIPAdminSite(AdminSite):
    def get_urls(self):
        urls = super(WIPAdminSite, self).get_urls()

        urls += [
            path('works_list', self.admin_view(WorksListView.as_view()), name='works_list'),
        ]

        return urls

admin.site = WIPAdminSite()

class WorkPhotoInline(admin.TabularInline):
    model = WorkPhoto
    extra = 3

class DesignerInline(admin.TabularInline):
    model = Designer

class WorkAdmin(admin.ModelAdmin):
    inlines = [ WorkPhotoInline, DesignerInline ]

admin.site.register(Work, WorkAdmin)

