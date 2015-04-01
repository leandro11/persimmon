# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0017_auto_20141205_1944'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='invoice',
            name='accountant',
        ),
    ]
