# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0006_staff_province'),
        ('member', '0014_auto_20141112_1636'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='enterprise',
            name='market_manager',
        ),
        migrations.AddField(
            model_name='enterprise',
            name='referee_manager',
            field=models.ForeignKey(related_name=b'referee_manager', verbose_name='\u63a8\u8350\u5e02\u573a\u7ecf\u7406', blank=True, to='management.Staff', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='enterprise',
            name='service_manager',
            field=models.ForeignKey(related_name=b'service_manager', verbose_name='\u670d\u52a1\u5e02\u573a\u7ecf\u7406', blank=True, to='management.Staff', null=True),
            preserve_default=True,
        ),
    ]
