# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0023_auto_20141127_1206'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bank',
            name='create_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='\u6ce8\u518c\u65f6\u95f4'),
        ),
        migrations.AlterField(
            model_name='bank',
            name='reference_count',
            field=models.IntegerField(default=0, verbose_name='\u6210\u529f\u63a8\u8350\u4f1a\u5458\u6570'),
        ),
    ]
