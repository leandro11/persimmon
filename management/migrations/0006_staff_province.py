# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0005_remove_staff_province'),
    ]

    operations = [
        migrations.AddField(
            model_name='staff',
            name='province',
            field=models.ManyToManyField(to='management.Province', verbose_name='\u7701\u4efd'),
            preserve_default=True,
        ),
    ]
