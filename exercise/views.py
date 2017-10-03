# -*- coding: utf-8 -*-

from itertools import chain
from calendar import month_name
from datetime import date, datetime
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render, redirect

from .calendar import Calendar
from .models import Jogging, Yoga, Weightlifting

def show(request, year=None, month=None):
    # Use current year and month unless specified otherwise
    if year is None or month is None:
        today = date.today()
        year, month = today.year, today.month
    else:
        year, month = int(year), int(month)

    jogging = Jogging.objects.filter(date__year=year, date__month=month)
    yoga = Yoga.objects.filter(date__year=year, date__month=month)
    weightlifting = (
        Weightlifting.objects.filter(date__year=year, date__month=month)
    )

    exercise_dates = [
        date
        for exercise in (jogging, yoga, weightlifting)
        for date in exercise.dates('date', 'day')
    ]

    exercise_calendar = Calendar(exercise_dates)
    context = {
        'year': year,
        'month': month_name[month],
        'calendar': exercise_calendar.formatmonth(year, month),
        'active': exercise_dates,
    }

    return render(request, 'exercise/calendar.html', context)

def calendar(request, year=None, month=None):
    """ Render exercise calendar for given month in HTML """
    # Use current year and month unless specified otherwise
    if year is None or month is None:
        today = date.today()
        year, month = today.year, today.month
    else:
        year, month = int(year), int(month)

    jogging = Jogging.objects.filter(date__year=year, date__month=month)
    yoga = Yoga.objects.filter(date__year=year, date__month=month)
    weightlifting = (
        Weightlifting.objects.filter(date__year=year, date__month=month)
    )

    exercise_dates = [
        entry.date for entry in chain(jogging, yoga, weightlifting)
    ]

    exercise_calendar = Calendar(exercise_dates)

    return HttpResponse(exercise_calendar.formatmonth(year, month))

def stats(request, year, month):
    """ Fetch exercise statistics for given month in JSON format """
    year, month = int(year), int(month)

    jogging = Jogging.objects.filter(date__year=year, date__month=month)
    yoga = Yoga.objects.filter(date__year=year, date__month=month)
    weightlifting = (
        Weightlifting.objects.filter(date__year=year, date__month=month)
    )

    entries = chain(jogging, yoga, weightlifting)
    data = serializers.serialize('json', entries)

    return HttpResponse(data)

def submit(request):
    entry_date = datetime.strptime(request.POST['date'], '%Y-%m-%d').date()

    if request.POST['jogging']:
        entry, created = Jogging.objects.update_or_create(
            date=entry_date,
            defaults={'kilometers': request.POST['jogging']},
        )
    else:
        Jogging.objects.filter(date=entry_date).delete()

    if request.POST['yoga']:
        entry, created = Yoga.objects.update_or_create(
            date=entry_date,
            defaults={'minutes': request.POST['yoga']},
        )
    else:
        Yoga.objects.filter(date=entry_date).delete()


    if request.POST['weightlifting']:
        entry, created = Weightlifting.objects.update_or_create(
            date=entry_date,
            defaults={'kilograms': request.POST['weightlifting']},
        )
    else:
        Weightlifting.objects.filter(date=entry_date).delete()

    return redirect('show')
