# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0004_auto_20141111_2328'),
        ('member', '0013_auto_20141112_0025'),
    ]

    operations = [
        migrations.AddField(
            model_name='bank',
            name='market_manager',
            field=models.ForeignKey(verbose_name='\u4e13\u5c5e\u5e02\u573a\u7ecf\u7406', blank=True, to='management.Staff', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='enterprise',
            name='market_manager',
            field=models.ForeignKey(verbose_name='\u4e13\u5c5e\u5e02\u573a\u7ecf\u7406', blank=True, to='management.Staff', null=True),
            preserve_default=True,
        ),
    ]
