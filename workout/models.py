# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class Workout(models.Model):
    date = models.DateField()
