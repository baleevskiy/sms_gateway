from __future__ import unicode_literals
import logging
from django.db import models

log = logging.getLogger(__name__)


class MessageStatus(object):
    NEW = 'new'
    PROCESSING = 'proc'
    SENT = 'sent'
    SCHEDULED = 'sched'
    ERROR = 'err'
    READ = 'read'
    UNREAD = 'unread'

    CHOICES = (
        (NEW, 'new'),
        (PROCESSING, 'proc'),
        (SENT, 'sent'),
        (SCHEDULED, 'sched'),
        (ERROR, 'err'),
        (READ, 'read'),
        (UNREAD, 'unread'),
    )


class Provider(models.Model):
    """
    Handlers are stored in DB, just to be able quickly manage them through web-interface
    """
    class_name = models.CharField(max_length=64, null=False)
    url = models.CharField(max_length=256, null=False)
    enabled = models.BooleanField(default=True)


class Message(models.Model):
    """
    base class for all sms
    """
    body = models.CharField(max_length=256)
    phone = models.CharField(max_length=20)
    status = models.CharField(choices=MessageStatus.CHOICES,
                              default=MessageStatus.NEW,
                              db_index=True,
                              max_length=32)


class MessageLog(models.Model):
    """
    Stores every try
    """
    message = models.ForeignKey('Message', related_name='logs')
    provider = models.ForeignKey('Provider', related_name='logs')
    status = models.CharField(choices=MessageStatus.CHOICES, max_length=32)
    request_data = models.TextField()
    response_data = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    timestamp_update = models.DateTimeField(auto_now=True)





