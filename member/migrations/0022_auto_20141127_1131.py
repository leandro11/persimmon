# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0021_auto_20141126_1606'),
    ]

    operations = [
        migrations.AddField(
            model_name='bank',
            name='reference_count',
            field=models.IntegerField(default=0, verbose_name='\u6210\u529f\u63a8\u8350\u6ce8\u518c\u6570'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='enterprise',
            name='reference_count',
            field=models.IntegerField(default=0, verbose_name='\u6210\u529f\u63a8\u8350\u6ce8\u518c\u6570'),
            preserve_default=True,
        ),
    ]
