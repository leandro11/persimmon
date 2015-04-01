# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0009_auto_20141201_1650'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='send_ems',
            field=models.CharField(max_length=50, unique=True, null=True, verbose_name='\u51fa\u7968\u5feb\u9012', blank=True),
            preserve_default=True,
        ),
    ]
