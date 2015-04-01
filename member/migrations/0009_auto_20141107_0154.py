# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0008_auto_20141104_1021'),
    ]

    operations = [
        migrations.AddField(
            model_name='bankcontactor',
            name='last_login',
            field=models.DateTimeField(verbose_name='\u4e0a\u6b21\u767b\u5f55\u65f6\u95f4', null=True, editable=False, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='bankoperator',
            name='last_login',
            field=models.DateTimeField(verbose_name='\u4e0a\u6b21\u767b\u5f55\u65f6\u95f4', null=True, editable=False, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='enterprisecontactor',
            name='last_login',
            field=models.DateTimeField(verbose_name='\u4e0a\u6b21\u767b\u5f55\u65f6\u95f4', null=True, editable=False, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='enterpriseoperator',
            name='last_login',
            field=models.DateTimeField(verbose_name='\u4e0a\u6b21\u767b\u5f55\u65f6\u95f4', null=True, editable=False, blank=True),
            preserve_default=True,
        ),
    ]
