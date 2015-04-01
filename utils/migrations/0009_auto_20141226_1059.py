# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('utils', '0008_auto_20141226_1050'),
    ]

    operations = [
        migrations.AddField(
            model_name='templateattachment',
            name='height',
            field=models.PositiveSmallIntegerField(help_text='\u56fe\u7247\u9ad8\u5ea6\uff0c\u4ec5\u5f53\u6587\u4ef6\u7c7b\u578b\u4e3a\u56fe\u7247\u65f6', max_length=10, null=True, verbose_name='\u9ad8\u5ea6', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='templateattachment',
            name='width',
            field=models.PositiveSmallIntegerField(help_text='\u56fe\u7247\u5bbd\u5ea6\uff0c\u4ec5\u5f53\u6587\u4ef6\u7c7b\u578b\u4e3a\u56fe\u7247\u65f6', max_length=10, null=True, verbose_name='\u5bbd\u5ea6', blank=True),
            preserve_default=True,
        ),
    ]
