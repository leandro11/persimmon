# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0025_remove_enterprisecontactor_groupname'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bankcontactor',
            name='groupname',
        ),
        migrations.RemoveField(
            model_name='bankoperator',
            name='groupname',
        ),
        migrations.RemoveField(
            model_name='enterpriseoperator',
            name='groupname',
        ),
    ]
