# -*- coding: utf-8 -*-

from django.contrib import admin

from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.core.mail import send_mail

from wagtail.contrib.settings.models import BaseSetting, register_setting

from .models import Stream

from feedler.refresh import refresh_streams

@register_setting
class FeedlySettings(BaseSetting):
    streams = models.ManyToManyField(Stream,
        help_text='Which streams to update')
    token = models.CharField(max_length=1024, blank=True,
        help_text='Access Token from feedly.com/v3/auth/dev')
    refresh = models.CharField(max_length=1024, blank=True,
        help_text='Refresh Token for automatic update (pro account)')
    class Meta:
        verbose_name = 'Feedly'

# @receiver(pre_save, sender=FeedlySettings)
# def handle_save_settings(sender, instance, *args, **kwargs):
#     if instance.token: refresh_streams(instance)
