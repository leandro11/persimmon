# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0010_zone_provinces'),
    ]

    operations = [
        migrations.AddField(
            model_name='staff',
            name='groupname',
            field=models.CharField(default='1', help_text='\u89d2\u8272\u540d\u79f0', max_length=20, verbose_name='\u89d2\u8272\u540d\u79f0', choices=[('\u5e02\u573a\u90e8\u603b\u7ecf\u7406', '\u5e02\u573a\u90e8\u603b\u7ecf\u7406'), ('\u533a\u57df\u5e02\u573a\u7ecf\u7406', '\u533a\u57df\u5e02\u573a\u7ecf\u7406'), ('\u5ba2\u670d\u90e8\u603b\u7ecf\u7406', '\u5ba2\u670d\u90e8\u603b\u7ecf\u7406'), ('\u533a\u57df\u5e02\u573a\u5ba2\u670d', '\u533a\u57df\u5e02\u573a\u5ba2\u670d'), ('\u603b\u7ecf\u7406', '\u603b\u7ecf\u7406'), ('\u6838\u7968\u5458', '\u6838\u7968\u5458'), ('\u7968\u636e\u4e3b\u7ba1', '\u7968\u636e\u4e3b\u7ba1'), ('\u4f1a\u8ba1', '\u4f1a\u8ba1')]),
            preserve_default=False,
        ),
    ]
