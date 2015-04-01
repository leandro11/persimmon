# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0008_auto_20141125_1720'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='zone',
            name='provinces',
        ),
    ]
