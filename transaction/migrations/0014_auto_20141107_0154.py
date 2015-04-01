# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0013_auto_20141107_0034'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transactiontype',
            name='name',
            field=models.CharField(default='\u4e94\u65e5\u8d34\u73b0', unique=True, max_length=20, verbose_name='\u8d34\u73b0\u670d\u52a1\u7c7b\u578b', choices=[('\u4e24\u65e5\u8d34\u73b0', '\u4e24\u65e5\u8d34\u73b0'), ('\u4e09\u65e5\u8d34\u73b0', '\u4e09\u65e5\u8d34\u73b0'), ('\u4e94\u65e5\u8d34\u73b0', '\u4e94\u65e5\u8d34\u73b0'), ('\u4e03\u65e5\u8d34\u73b0', '\u4e03\u65e5\u8d34\u73b0')]),
        ),
    ]
