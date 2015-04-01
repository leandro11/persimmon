# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0036_auto_20141229_1940'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bank',
            name='expired_date',
            field=models.DateTimeField(null=True, verbose_name='\u5408\u4f5c\u622a\u6b62\u65f6\u95f4'),
        ),
    ]
