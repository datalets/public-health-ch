# -*- coding: utf-8 -*-

import requests, json, codecs

from django.contrib import admin

from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.core.mail import send_mail

from wagtail.contrib.settings.models import BaseSetting, register_setting

from .models import Entry, Stream
import feedler.feedparser as feedparser

import logging
logger = logging.getLogger('feedler')

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
    feedly_stream = models.ManyToManyField(Stream)
    class Meta:
        verbose_name = 'Feedly'

API_BASEURL = 'https://cloud.feedly.com/v3/streams/contents?streamId='

@receiver(pre_save, sender=FeedlySettings)
def handle_save_settings(sender, instance, *args, **kwargs):
    if instance.feedly_auth:
        streams = instance.feedly_stream.all()
        for stream in streams:
            # Start a request to download the feed
            logger.info("Processing stream %s" % stream.title)
            url = API_BASEURL + stream.ident
            headers = {
                'Authorization': 'OAuth ' + instance.feedly_auth
            }
            contents = requests.get(url, headers=headers).json()
            if 'errorMessage' in contents:
                raise PermissionError(contents['errorMessage'])
            for raw_entry in contents['items']:
                eid = raw_entry['id']
                # Create or update data
                try:
                    entry = Entry.objects.get(entry_id=eid)
                    logger.info("Updating entry '%s'" % eid)
                except Entry.DoesNotExist:
                    logger.info("Adding entry '%s'" % eid)
                    entry = Entry()
                entry = feedparser.parse(entry, raw_entry, stream)
                entry.save()
