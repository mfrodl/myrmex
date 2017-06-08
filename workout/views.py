# -*- coding: utf-8 -*-

from datetime import date
from calendar import month_name
from django.shortcuts import render, redirect

from .workout_calendar import WorkoutCalendar
from .models import Workout

def show(request, year=None, month=None):
    # Use current year and month unless specified otherwise
    if year is None or month is None:
        today = date.today()
        year, month = today.year, today.month
    else:
        year, month = int(year), int(month)

    month_workouts = Workout.objects.filter(date__year=year, date__month=month)
    workout_dates = [workout.date for workout in month_workouts]

    workout_calendar = WorkoutCalendar(workout_dates)
    context = {
        'year': year,
        'month': month_name[month],
        'calendar': workout_calendar.formatmonth(year, month),
        'active': workout_dates,
    }

    print(repr(year), repr(month))
    return render(request, 'workout/calendar.html', context)

def toggle(request, year, month, day):
    day_date = date(int(year), int(month), int(day))
    try:
        entry = Workout.objects.get(date=day_date)
        entry.delete()
    except:
        Workout.objects.create(date=day_date)
    return redirect('show', year=year, month=month)
