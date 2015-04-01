# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0017_auto_20141107_0336'),
    ]

    operations = [
        migrations.RenameField(
            model_name='transactionoperation',
            old_name='operator_type',
            new_name='operator_member_type',
        ),
        migrations.RenameField(
            model_name='transactionoperation',
            old_name='operator',
            new_name='operator_user',
        ),
    ]
