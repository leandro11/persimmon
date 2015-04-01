# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0007_auto_20141125_1653'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='province',
            name='zone',
        ),
        migrations.AddField(
            model_name='zone',
            name='provinces',
            field=models.ForeignKey(default=1, verbose_name='\u5305\u542b\u7701\u4efd', to='management.Province'),
            preserve_default=False,
        ),
    ]
