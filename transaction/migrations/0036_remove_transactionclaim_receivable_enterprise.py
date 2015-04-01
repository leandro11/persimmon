# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0035_auto_20141107_1908'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transactionclaim',
            name='receivable_enterprise',
        ),
    ]
