# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0004_auto_20141106_1812'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transactionoperation',
            name='need_ems',
        ),
        migrations.RemoveField(
            model_name='transactionoperation',
            name='need_upload',
        ),
    ]
