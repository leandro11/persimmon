# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0024_auto_20141127_2233'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='enterprisecontactor',
            name='groupname',
        ),
    ]
