# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0003_auto_20141106_1810'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transactionoperation',
            name='claim',
        ),
        migrations.RemoveField(
            model_name='transactionoperation',
            name='name',
        ),
    ]
