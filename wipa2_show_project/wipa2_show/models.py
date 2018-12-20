# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import uuid

from django.core.mail import EmailMessage
from django.core.validators import RegexValidator
from django.db import models


class ExhibitionConfirmation(models.Model):
    artist_name = models.CharField(max_length=200)
    artist_email = models.EmailField()
    phone_regex = RegexValidator(regex=r'^(\+?\d{1,2}\s)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}$',
                                 message="Invalid phone number.")
    artist_phone = models.CharField(validators=(phone_regex,), max_length=20)

    exhibition_names = models.TextField()
    exhibition_statement = models.TextField(blank=True)
    artist_bio = models.TextField()
    installation_instructions = models.TextField()

    def send_email(self):
        email = EmailMessage(
            'Works in Progress 2019: Exhibition Confirmed',
            f"""
                <strong>Artist Name:</strong> {self.artist_name}<br>
                <strong>Artist Email:</strong> {self.artist_email}<br>
                <strong>Artist Phone:</strong> {self.artist_phone}<br>
                <br><br>
                <strong>Work Name(s):</strong> {self.exhibition_names}<br>
                <strong>Work Statement:</strong> {self.exhibition_statement}<br>
                <strong>Artist Bio:</strong> {self.artist_bio}
                <br><br>
                <strong>Installation Instructions:</strong> {self.installation_instructions}
            """,
            'wipa2.show@gmail.com',
            [''],
            [''],
            reply_to=['wipa2.show@gmail.com'],
            headers={},
        )

        for photo_exhibition in self.photo_exhibition.all():
            email.attach_file(photo_exhibition.exhibition_photo.path)
        
        email.content_subtype = "html"

        email.send()


class ExhibitionPhoto(models.Model):
    def images_directory_path(instance, filename):
        return '/'.join(['exhibition_photos', str(instance.exhibition.id), str(uuid.uuid4().hex + ".png")])

    exhibition_photo = models.ImageField(upload_to=images_directory_path)
    exhibition = models.ForeignKey(ExhibitionConfirmation, related_name='photo_exhibition', on_delete=models.CASCADE)

    def get_type(self):
        try:
            magic_no = self.exhibition_photo.read(4)
        except FileNotFoundError:
            return 'MISSING FILE'

        result = 'UNKNOWN'
        if magic_no == b'\x89\x50\x4e\x47':
            result = 'PNG'
        elif magic_no == b'\x25\x50\x44\x46':
            result = 'PDF'
        elif magic_no == b'\x47\x49\x46\x38':
            result = 'GIF'
        elif magic_no == b'\x50\x4b\x03\x04' or magic_no == b'\x50\x4b\x05\x06' or magic_no == b'\x50\x4b\x07\x08':
            result = 'ZIP'
        elif magic_no[:2] == b'\xFF\xD8':
            # not quite right but close enough for now
            result = 'JPG'

        self.exhibition_photo.seek(0)
        return result


class Work(models.Model):
    work_title = models.CharField(max_length=200)
    work_dimensions = models.CharField(max_length=200)
    work_description = models.TextField()
    work_display_requirements = models.TextField()
    year_regex = RegexValidator(regex=r'^\d{4}$', message="Year must be entered in YYYY format")
    work_year = models.CharField(validators=(year_regex,), max_length=4)

    def get_designer(self):
        queryset = Designer.objects.filter(work__id=self.id)
        
        if not queryset:
            return None
        else:
            return queryset[0]

    def get_designer_info(self):
        designer = self.get_designer()

        if not designer:
            return {
                "name": "unknown",
                "phone": "unknown",
                "email": "unknown",
            }

        return {
            "name": designer.designer_name,
            "phone": designer.designer_phone_number,
            "email": designer.designer_email,
        }

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

    def get_type(self):
        try:
            magic_no = self.work_photo.read(4)
        except FileNotFoundError:
            return 'MISSING FILE'

        result = 'UNKNOWN'
        if magic_no == b'\x89\x50\x4e\x47':
            result = 'PNG'
        elif magic_no == b'\x25\x50\x44\x46':
            result = 'PDF'
        elif magic_no == b'\x47\x49\x46\x38':
            result = 'GIF'
        elif magic_no == b'\x50\x4b\x03\x04' or magic_no == b'\x50\x4b\x05\x06' or magic_no == b'\x50\x4b\x07\x08':
            result = 'ZIP'
        elif magic_no[:2] == b'\xFF\xD8':
            # not quite right but close enough for now
            result = 'JPG'

        self.work_photo.seek(0)
        return result