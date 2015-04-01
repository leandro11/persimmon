# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='formerholder',
            old_name='order',
            new_name='transaction',
        ),
        migrations.RenameField(
            model_name='transactionoperation',
            old_name='order',
            new_name='transaction',
        ),
    ]
