# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.views import generic

from .forms import WorkForm
from .models import Work, WorkPhoto


def index(request):
    form = WorkForm({})
    context = {'form': form}
    return render(request, 'index.html', context)


class WorksListView(generic.ListView):
    template_name = 'works_list.html'
    context_object_name = 'works_list'

    def get_queryset(self):
        return Work.objects.all()

def submit(request):
    def _valid_photos(files):
        if len(files) == 0:
            return False, "No photos uploaded"
        
        for file in files.getlist('images'):
            if file.size > 1024 * 1024 * 10: # 10 MB max size
                return False, "Max size for photos is 10MB"
        
        return True, ""

    form = WorkForm({})
    context = {'form': form}

    print(request.POST)
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = WorkForm(request.POST)
        # check whether it's valid:
        valid_photos, photo_error = _valid_photos(request.FILES)
        if form.is_valid() and valid_photos:
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            work = form.save()
            for photo in request.FILES.getlist('images'):
                print(photo)
                print(dir(photo))
                image = WorkPhoto(
                    work=work,
                    work_photo=photo
                )
                image.save()

            return render(request, 'thanks.html')
        return render(request, 'index.html', {'posted': True, 'form': form, 'photo_error': photo_error})
    else:
        return render(request, 'index.html', context)
