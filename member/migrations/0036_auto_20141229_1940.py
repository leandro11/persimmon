# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0035_auto_20141229_1756'),
    ]

    operations = [
        migrations.AlterField(
            model_name='enterprise',
            name='create_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='\u6ce8\u518c\u65f6\u95f4'),
        ),
    ]
