# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=32, verbose_name='title')),
                ('description', models.CharField(max_length=100, verbose_name='description')),
            ],
            options={
                'ordering': ('title',),
                'verbose_name': 'event',
                'verbose_name_plural': 'events',
            },
        ),
        migrations.CreateModel(
            name='EventType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('abbr', models.CharField(unique=True, max_length=4, verbose_name='abbreviation')),
                ('label', models.CharField(max_length=50, verbose_name='label')),
            ],
            options={
                'verbose_name': 'event type',
                'verbose_name_plural': 'event types',
            },
        ),
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('note', models.TextField(verbose_name='note')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('object_id', models.PositiveIntegerField(verbose_name='object id')),
                ('content_type', models.ForeignKey(verbose_name='content type', to='contenttypes.ContentType')),
            ],
            options={
                'verbose_name': 'note',
                'verbose_name_plural': 'notes',
            },
        ),
        migrations.CreateModel(
            name='Occurrence',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start_time', models.DateTimeField(verbose_name='start time')),
                ('end_time', models.DateTimeField(verbose_name='end time')),
                ('event', models.ForeignKey(editable=False, to='swingtime.Event', verbose_name='event')),
            ],
            options={
                'ordering': ('start_time', 'end_time'),
                'verbose_name': 'occurrence',
                'verbose_name_plural': 'occurrences',
            },
        ),
        migrations.AddField(
            model_name='event',
            name='event_type',
            field=models.ForeignKey(verbose_name='event type', to='swingtime.EventType'),
        ),
    ]
