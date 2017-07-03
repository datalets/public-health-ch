# -*- coding: utf-8 -*-

import requests, json, codecs

from django.contrib import admin

from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.core.mail import send_mail

from wagtail.contrib.settings.models import BaseSetting, register_setting

# Feedly integration module

@register_setting
class FeedlySettings(BaseSetting):
    feedly_auth = models.TextField(
        help_text='Your developer authorization key', blank=True)
    feedly_pages = models.IntegerField(
        choices=(
            (1, '2'),
            (2, '5'),
            (3, '10'),
            (4, '50'),
        ), blank=True, null=True,
        help_text='How many pages to fetch?'
    )
    feedly_stream = models.TextField(
        help_text='Stream ID to fetch', blank=True)
    class Meta:
        verbose_name = 'Feedly'

@receiver(pre_save, sender=FeedlySettings)
def handle_save_settings(sender, instance, *args, **kwargs):
    if instance.feedly_stream and instance.feedly_auth:
        entries = []
        url = 'https://cloud.feedly.com/v3/streams/contents?streamId='
        url = url + instance.feedly_stream
        headers = {
            'Authorization': 'OAuth '+instance.feedly_auth
        }
        contents = requests.get(url, headers=headers).json()
        if 'errorMessage' in contents:
            raise PermissionError(contents['errorMessage'])
        for raw_entry in contents['items']:
            entry = Entry(raw_entry)
            entries.append(entry)
        print(json.dumps(entries))
