# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0030_auto_20141226_1654'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bankattachment',
            name='creator',
            field=models.ForeignKey(verbose_name='\u64cd\u4f5c\u7528\u62371', to=settings.AUTH_USER_MODEL),
        ),
    ]
