# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class Keys(models.Model):
    user = models.CharField(max_length=30)
    key_name = models.CharField(max_length=30)
    release = models.IntegerField(default = 0)
    timestamp = models.BigIntegerField(default =0)
