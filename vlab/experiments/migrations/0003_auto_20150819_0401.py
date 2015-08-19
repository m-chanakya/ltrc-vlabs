# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('experiments', '0002_auto_20150819_0248'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='experimentstage',
            unique_together=set([('experiment', 'name')]),
        ),
    ]
