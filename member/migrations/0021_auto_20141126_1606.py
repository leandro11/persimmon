# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0020_auto_20141125_1117'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registerinvitationcode',
            name='market_manager',
            field=models.ForeignKey(verbose_name='\u5e02\u573a\u7ecf\u7406', blank=True, to='management.Staff', null=True),
        ),
    ]
