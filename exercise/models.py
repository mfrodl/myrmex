# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class Exercise(models.Model):
    date = models.DateField()

    class Meta:
        abstract = True


class Jogging(Exercise):
    kilometers = models.FloatField()


class Weightlifting(Exercise):
    kilograms = models.FloatField()


class Yoga(Exercise):
    minutes = models.FloatField()
