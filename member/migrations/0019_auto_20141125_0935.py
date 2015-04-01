# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0018_auto_20141125_0846'),
    ]

    operations = [
        migrations.AddField(
            model_name='registerinvitationcode',
            name='contactor_email',
            field=models.EmailField(default='1@1.com', max_length=50, verbose_name='\u4e3b\u8054\u7edc\u4eba\u90ae\u7bb1'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='registerinvitationcode',
            name='contactor_name',
            field=models.CharField(default='name', max_length=20, verbose_name='\u4e3b\u8054\u7edc\u4eba\u59d3\u540d'),
            preserve_default=False,
        ),
    ]
