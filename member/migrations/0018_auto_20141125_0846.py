# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0017_auto_20141125_0837'),
    ]

    operations = [
        migrations.AddField(
            model_name='registerinvitationcode',
            name='referee_member_id',
            field=models.BigIntegerField(null=True, verbose_name='\u63a8\u8350\u4f1a\u5458\u7f16\u53f7', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='registerinvitationcode',
            name='referee_member_type',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='\u63a8\u8350\u4f1a\u5458\u7c7b\u578b', choices=[(b'Bank', '\u94f6\u884c\u4f1a\u5458'), (b'Enterprise', '\u4f01\u4e1a\u4f1a\u5458')]),
            preserve_default=True,
        ),
    ]
