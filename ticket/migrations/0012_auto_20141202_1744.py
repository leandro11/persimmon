# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0011_auto_20141202_1739'),
    ]

    operations = [
        migrations.RenameField(
            model_name='invoicelog',
            old_name='oprator',
            new_name='operator',
        ),
        migrations.RenameField(
            model_name='ticketelog',
            old_name='oprator',
            new_name='operator',
        ),
    ]
