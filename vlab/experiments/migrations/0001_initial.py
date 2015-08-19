# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Experiment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=200)),
                ('lang', models.CharField(max_length=200)),
                ('visit_count', models.IntegerField(default=0)),
                ('completed_count', models.IntegerField(default=0)),
                ('prescribed_time', models.IntegerField(default=0)),
                ('max_score', models.IntegerField(default=0)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ExperimentStage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=200)),
                ('visit_count', models.IntegerField(default=0)),
                ('completed_count', models.IntegerField(default=0)),
                ('prescribed_time', models.IntegerField(default=0)),
                ('max_score', models.IntegerField()),
                ('experiment', models.ForeignKey(to='experiments.Experiment')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Participant',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('time', models.IntegerField(default=0)),
                ('score', models.IntegerField(default=0)),
                ('mode', models.CharField(max_length=10, choices=[(b'free style', b'test mode')])),
                ('experiment', models.ForeignKey(to='experiments.Experiment')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ParticipantStage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('time', models.IntegerField(default=0)),
                ('score', models.IntegerField(default=0)),
                ('attempts', models.IntegerField(default=0)),
                ('participant', models.ForeignKey(to='experiments.Participant')),
                ('stage', models.ForeignKey(to='experiments.ExperimentStage')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
