# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0013_auto_20141128_1121'),
    ]

    operations = [
        migrations.RenameField(
            model_name='staff',
            old_name='groupname',
            new_name='position',
        ),
    ]
