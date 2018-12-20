# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import calendar
import time

from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.views import generic

import stripe

from .forms import WorkForm, ExhibitionForm
from .models import Work, WorkPhoto, Designer, ExhibitionConfirmation, ExhibitionPhoto


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


def exhibit(request):
    def _valid_photos(files):
        if len(files.getlist('images')) == 0:
            return False, "No photos uploaded."
        elif len(files.getlist('images')) > 5:
            return False, "No more than 5 photos, please."
        
        for file in files.getlist('images'):
            if file.size > 1024 * 1024 * 3.2: # 3.2MB max size
                return False, "Max size for photos is 3.2MB each."
        
        return True, ""

    form = ExhibitionForm({})
    context = {'form': form}

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ExhibitionForm(request.POST)
        valid_photos, photo_error = _valid_photos(request.FILES)
        if form.is_valid() and valid_photos:
            # Token is created using Checkout or Elements!	
            # Get the payment token ID submitted by the form:	
            token = request.POST['stripeToken']	
 
            try:	
                charge = stripe.Charge.create(	
                    amount=2000,	
                    currency='usd',	
                    description=f'wipa2.show exhibition fee -- {form.cleaned_data['artist_email']}',	
                    source=token,	
                )	
            except Exception as e:	
                print(e)
                return render(request, 'exhibition.html', {'posted': True, 'form': form, 'charge_error': 'An error occurred processing your credit card.'})	

            if charge['status'] != 'succeeded':	
                return render(request, 'exhibition.html', {'posted': True, 'form': form, 'charge_error': charge['failure_message']})	

            exhibition = form.save()

            for photo in request.FILES.getlist('images'):
                image = ExhibitionPhoto(
                    exhibition=exhibition,
                    exhibition_photo=photo
                )
                image.save()

            exhibition.send_email()
            return render(request, 'exhibition_thanks.html')
        return render(request, 'exhibition.html', {'posted': True, 'form': form, 'photo_error': photo_error})
    else:
        return render(request, 'exhibition.html', context)


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
            work = form.save()

            artist = Designer(designer_name=request.POST.get('artist_name'),
                              designer_email=request.POST.get('artist_email'),
                              designer_phone_number=request.POST.get('artist_phone'))
            artist.work = work
            artist.save()

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
