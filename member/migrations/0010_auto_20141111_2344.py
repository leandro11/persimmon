# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0009_auto_20141107_0154'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bankcontactor',
            name='fax_number',
        ),
        migrations.RemoveField(
            model_name='bankoperator',
            name='fax_number',
        ),
        migrations.RemoveField(
            model_name='enterprisecontactor',
            name='fax_number',
        ),
        migrations.RemoveField(
            model_name='enterpriseoperator',
            name='fax_number',
        ),
    ]
