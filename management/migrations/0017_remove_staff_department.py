# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0016_remove_staff_password'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='staff',
            name='department',
        ),
    ]
