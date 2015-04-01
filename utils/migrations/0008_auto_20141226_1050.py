# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('utils', '0007_auto_20141223_1709'),
    ]

    operations = [
        migrations.AddField(
            model_name='templateattachment',
            name='create_time',
            field=models.DateTimeField(default=datetime.datetime(2014, 12, 26, 10, 50, 0, 118000), verbose_name='\u521b\u5efa\u65f6\u95f4', auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='templateattachment',
            name='creator',
            field=models.ForeignKey(verbose_name='\u64cd\u4f5c\u7528\u6237', blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='templateattachment',
            name='thumbnail',
            field=models.FileField(help_text='\u4ec5\u56fe\u7247\u7c7b\u578b\u6587\u4ef6\u81ea\u52a8\u751f\u6210', upload_to=b'./template_document/thumbnail', null=True, verbose_name='\u7f29\u7565\u6587\u4ef6', blank=True),
            preserve_default=True,
        ),
    ]
