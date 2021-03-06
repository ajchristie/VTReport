# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible
from django.db import models
from django.contrib.sessions.models import Session
import datetime


@python_2_unicode_compatible
class VTReport(models.Model):
    md5 = models.CharField(max_length=32)
    sha1 = models.CharField(max_length=40)
    sha256 = models.CharField(max_length=64)
    num_engines = models.PositiveIntegerField(default=0)
    fortinet_name = models.CharField(default="")
    scandate = models.DateTimeField()
    res_code = models.SmallIntegerField(null=True,default=null)
    queried = models.DateTimeField(auto_now_add=True)
    sessions = models.ManyToManyField(Session)

    def __str__(self):
        return "VirusTotal report for MD5:" + str(self.md5)

    def is_recent(self):
        return timezone.now() - datetime.timedelta(days=1) <= self.queried
