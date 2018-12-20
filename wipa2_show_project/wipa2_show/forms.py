# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

from .models import Work, ExhibitionConfirmation

class ExhibitionForm(forms.ModelForm):
    class Meta:
        model = ExhibitionConfirmation
        fields = [
            'artist_name',
            'artist_email',
            'artist_phone',
            'exhibition_names',
            'exhibition_statement',
            'artist_bio',
            'installation_instructions',
        ]

    artist_name = forms.CharField(label='Name', max_length=200)
    artist_email = forms.CharField(label='Email', max_length=200)
    phone_regex = RegexValidator(regex=r'^(\+?\d{1,2}\s)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}$',
                                 message="Invalid phone number.")
    artist_phone = forms.CharField(label='Phone', max_length=20, validators=[phone_regex])
    exhibition_names = forms.CharField(label='Name of Work(s)', max_length=2500, widget=forms.Textarea, required=False)
    exhibition_statement = forms.CharField(label='Description of Work(s)', max_length=2500, widget=forms.Textarea, required=False)
    artist_bio = forms.CharField(label='Artist Bio', max_length=2500, widget=forms.Textarea)
    installation_instructions = forms.CharField(label='Installation Instructions', max_length=2500, widget=forms.Textarea)


class WorkForm(forms.ModelForm):
    class Meta:
        model = Work
        fields = [
            'artist_name',
            'artist_email',
            'artist_phone',
            'work_title',
            'work_dimensions',
            'work_description',
            'work_display_requirements',
            'work_year']

    artist_name = forms.CharField(label='Name', max_length=200)
    artist_email = forms.CharField(label='Email', max_length=200)
    phone_regex = RegexValidator(regex=r'^(\+?\d{1,2}\s)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}$',
                                 message="Invalid phone number.")
    artist_phone = forms.CharField(label='Phone', max_length=20, validators=[phone_regex])
    work_title = forms.CharField(label='Title of Work', max_length=200)
    work_dimensions = forms.CharField(label='Dimensions', max_length=200)
    work_description = forms.CharField(label='Description of Work', max_length=2500, widget=forms.Textarea)
    work_display_requirements = forms.CharField(label='How is the work displayed?', max_length=2500, widget=forms.Textarea)
    year_regex = RegexValidator(regex=r'^\d{4}$', message="Year must be entered in YYYY format")
    work_year = forms.CharField(label='Year Created', max_length=4, validators=[year_regex])
