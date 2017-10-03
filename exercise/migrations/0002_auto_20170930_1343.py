# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-30 13:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exercise', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Jogging',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('kilometers', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Weightlifting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('kilograms', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Yoga',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('minutes', models.FloatField()),
            ],
        ),
        migrations.DeleteModel(
            name='Workout',
        ),
    ]
