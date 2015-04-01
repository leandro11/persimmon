# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0006_staff_province'),
        ('member', '0015_auto_20141124_1659'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bank',
            name='market_manager',
        ),
        migrations.AddField(
            model_name='bank',
            name='referee_manager',
            field=models.ForeignKey(related_name=b'bank_referee_manager', verbose_name='\u63a8\u8350\u5e02\u573a\u7ecf\u7406', blank=True, to='management.Staff', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='bank',
            name='service_manager',
            field=models.ForeignKey(related_name=b'bank_service_manager', verbose_name='\u670d\u52a1\u5e02\u573a\u7ecf\u7406', blank=True, to='management.Staff', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='enterprise',
            name='referee_manager',
            field=models.ForeignKey(related_name=b'enterprise_referee_manager', verbose_name='\u63a8\u8350\u5e02\u573a\u7ecf\u7406', blank=True, to='management.Staff', null=True),
        ),
        migrations.AlterField(
            model_name='enterprise',
            name='service_manager',
            field=models.ForeignKey(related_name=b'enterprise_service_manager', verbose_name='\u670d\u52a1\u5e02\u573a\u7ecf\u7406', blank=True, to='management.Staff', null=True),
        ),
    ]
