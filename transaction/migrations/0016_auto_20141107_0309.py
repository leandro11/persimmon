# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0015_auto_20141107_0238'),
    ]

    operations = [
        migrations.RenameField(
            model_name='transactionmetaoperation',
            old_name='trsaction_type',
            new_name='transaction_type',
        ),
        migrations.AlterUniqueTogether(
            name='transactionmetaoperation',
            unique_together=set([('transaction_type', 'sequence')]),
        ),
    ]
