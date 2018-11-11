# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import uuid

from django.core.validators import RegexValidator
from django.db import models

class Work(models.Model):
    work_title = models.CharField(max_length=200)
    work_dimensions = models.CharField(max_length=200)
    work_description = models.TextField()
    work_display_requirements = models.TextField()
    year_regex = RegexValidator(regex=r'^\d{4}$', message="Year must be entered in YYYY format")
    work_year = models.CharField(validators=(year_regex,), max_length=4)

class Designer(models.Model):
    designer_name = models.CharField(max_length=200)
    designer_email = models.EmailField()
    phone_regex = RegexValidator(regex=r'^(\+?\d{1,2}\s)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}$',
                                 message="Invalid phone number.")
    designer_phone_number = models.CharField(validators=(phone_regex,), max_length=20)
    work = models.OneToOneField(
        Work,
        on_delete=models.CASCADE,
        primary_key=False,
    )

class WorkPhoto(models.Model):
    def images_directory_path(instance, filename):
        return '/'.join(['work_photos', str(instance.work.id), str(uuid.uuid4().hex + ".png")])

    work_photo = models.ImageField(upload_to=images_directory_path)
    work = models.ForeignKey(Work, related_name='photo_work', on_delete=models.CASCADE)