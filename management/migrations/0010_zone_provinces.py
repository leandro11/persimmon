# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0009_remove_zone_provinces'),
    ]

    operations = [
        migrations.AddField(
            model_name='zone',
            name='provinces',
            field=models.ManyToManyField(to='management.Province', verbose_name='\u5305\u542b\u7701\u4efd'),
            preserve_default=True,
        ),
    ]
