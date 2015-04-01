# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0007_auto_20141104_1018'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='enterpriseoperator',
            unique_together=set([('user', 'enterprise')]),
        ),
    ]
