# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0011_staff_groupname'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='staff',
            name='position',
        ),
        migrations.AlterField(
            model_name='staff',
            name='groupname',
            field=models.CharField(help_text='\u5fc5\u586b', max_length=30, verbose_name='\u804c\u4f4d', choices=[('\u5e02\u573a\u90e8\u603b\u7ecf\u7406', '\u5e02\u573a\u90e8\u603b\u7ecf\u7406'), ('\u533a\u57df\u5e02\u573a\u7ecf\u7406', '\u533a\u57df\u5e02\u573a\u7ecf\u7406'), ('\u5ba2\u670d\u90e8\u603b\u7ecf\u7406', '\u5ba2\u670d\u90e8\u603b\u7ecf\u7406'), ('\u533a\u57df\u5e02\u573a\u5ba2\u670d', '\u533a\u57df\u5e02\u573a\u5ba2\u670d'), ('\u603b\u7ecf\u7406', '\u603b\u7ecf\u7406'), ('\u6838\u7968\u5458', '\u6838\u7968\u5458'), ('\u7968\u636e\u4e3b\u7ba1', '\u7968\u636e\u4e3b\u7ba1'), ('\u4f1a\u8ba1', '\u4f1a\u8ba1')]),
        ),
    ]
