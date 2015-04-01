# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0039_auto_20141112_1009'),
    ]

    operations = [
        migrations.AddField(
            model_name='transactionclaim',
            name='create_time',
            field=models.DateTimeField(default=datetime.datetime(2014, 11, 12, 15, 36, 9, 396000), verbose_name='\u521b\u5efa\u65f6\u95f4', auto_now_add=True),
            preserve_default=False,
        ),
    ]
