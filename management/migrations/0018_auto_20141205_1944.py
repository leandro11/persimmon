# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0017_remove_staff_department'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='staff',
            name='date_joined',
        ),
        migrations.RemoveField(
            model_name='staff',
            name='is_active',
        ),
        migrations.RemoveField(
            model_name='staff',
            name='last_login',
        ),
    ]
