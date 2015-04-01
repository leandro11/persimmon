# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0019_auto_20141125_0935'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registerinvitationcode',
            name='market_manager',
            field=models.ForeignKey(verbose_name='\u5e02\u573a\u7ecf\u7406', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='registerinvitationcode',
            name='member_name',
            field=models.CharField(max_length=50, verbose_name='\u4f1a\u5458\u540d\u79f0'),
        ),
    ]
