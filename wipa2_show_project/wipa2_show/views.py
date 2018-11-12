# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import calendar
import time

from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.views import generic

import stripe

from .forms import WorkForm
from .models import Work, WorkPhoto


def _in_entry_period():
    return calendar.timegm(time.gmtime()) <= 1544417999

def index(request):
    form = WorkForm({})
    context = {'form': form, 'in_entry_period': _in_entry_period()}
    return render(request, 'index.html', context)


class WorksListView(generic.ListView):
    template_name = 'works_list.html'
    context_object_name = 'works_list'

    def get_queryset(self):
        return Work.objects.all()


def submit(request):
    def _valid_photos(files):
        if len(files.getlist('images')) == 0:
            return False, "No photos uploaded."
        elif len(files.getlist('images')) > 5:
            return False, "No more than 5 photos, please."
        
        for file in files.getlist('images'):
            if file.size > 1024 * 1024 * 3.2: # 3.2MB max size
                return False, "Max size for photos is 3.2MB each."
        
        return True, ""

    form = WorkForm({})
    context = {'form': form, 'in_entry_period': _in_entry_period()}

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = WorkForm(request.POST)
        valid_photos, photo_error = _valid_photos(request.FILES)
        if form.is_valid() and valid_photos and _in_entry_period():
            # Token is created using Checkout or Elements!
            # Get the payment token ID submitted by the form:
            token = request.POST['stripeToken']

            try:
                charge = stripe.Charge.create(
                    amount=1000,
                    currency='usd',
                    description='wipa2.show submission fee',
                    source=token,
                )
            except:
                return render(request, 'index.html', {'posted': True, 'form': form, 'charge_error': 'An error occurred processing your credit card.', 'in_entry_period': _in_entry_period()})

            if charge['status'] != 'succeeded':
                return render(request, 'index.html', {'posted': True, 'form': form, 'charge_error': charge['failure_message'], 'in_entry_period': _in_entry_period()})

            work = form.save()
            for photo in request.FILES.getlist('images'):
                image = WorkPhoto(
                    work=work,
                    work_photo=photo
                )
                image.save()

            return render(request, 'thanks.html')
        return render(request, 'index.html', {'posted': True, 'form': form, 'photo_error': photo_error, 'in_entry_period': _in_entry_period()})
    else:
        return render(request, 'index.html', context)
