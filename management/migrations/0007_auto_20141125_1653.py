# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0006_staff_province'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='staff',
            name='province',
        ),
        migrations.AddField(
            model_name='staff',
            name='zone',
            field=models.ManyToManyField(to='management.Zone', verbose_name='\u8d1f\u8d23\u533a\u57df'),
            preserve_default=True,
        ),
    ]
