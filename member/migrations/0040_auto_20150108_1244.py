# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0039_auto_20150106_1149'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bank',
            name='execution_agreements',
        ),
        migrations.RemoveField(
            model_name='bank',
            name='strategic_agreements',
        ),
        migrations.RemoveField(
            model_name='enterprise',
            name='licence',
        ),
        migrations.RemoveField(
            model_name='enterprise',
            name='organization_code',
        ),
        migrations.RemoveField(
            model_name='enterprise',
            name='tax_registration',
        ),
    ]
