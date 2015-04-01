# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0018_auto_20141107_0339'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transactionoperation',
            name='operate_type',
        ),
    ]
