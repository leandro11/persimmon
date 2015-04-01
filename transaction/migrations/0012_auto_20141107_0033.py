# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0011_auto_20141106_2320'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='FormerHolder',
            new_name='TicketFormerHolder',
        ),
    ]
