# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0045_auto_20141127_1212'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transactionclaim',
            name='ticket_deadline',
        ),
    ]
