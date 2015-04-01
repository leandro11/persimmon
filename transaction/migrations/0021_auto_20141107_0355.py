# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0020_auto_20141107_0348'),
    ]

    operations = [
        migrations.RenameField(
            model_name='transactionmetaoperation',
            old_name='operator',
            new_name='operator_member',
        ),
    ]
