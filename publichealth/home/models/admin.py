# -*- coding: utf-8 -*-

from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.core.mail import send_mail

from wagtail.contrib.settings.models import BaseSetting, register_setting

# A simple feedback module built into the site admin

@register_setting(icon='help')
class DataletsSettings(BaseSetting):
    feedback_question = models.TextField(verbose_name='Name',
        help_text='Who should we reply to for questions?', blank=True)
    feedback_status = models.IntegerField(verbose_name='Rating',
        choices=(
            (1, u'★'),
            (2, u'★'*2),
            (3, u'★'*3),
            (4, u'★'*4),
            (5, u'★'*5),
        ), blank=True, null=True,
        help_text='How are you enjoying Wagtail?'
    )
    feedback_comment = models.TextField(verbose_name='Comments..',
        help_text='Any questions or general feedback', blank=True)
    class Meta:
        verbose_name = 'Datalets'

@receiver(pre_save, sender=DataletsSettings)
def handle_save_settings(sender, instance, *args, **kwargs):
    if instance.feedback_status is not None:
        send_mail("Response from Wagtail",
            "%s\n--\n%s\n--\n%s" % (
                str(instance.feedback_status),
                instance.feedback_question,
                instance.feedback_comment,
            ), "wagtail@datalets.ch",
            [ "support@datalets.ch" ]
        )
        instance.feedback_status = None
        instance.feedback_question = ""
        instance.feedback_comment = ""
        instance.save()
