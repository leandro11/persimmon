# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import member.models


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0032_auto_20141226_1657'),
    ]

    operations = [
        migrations.AlterField(
            model_name='enterpriseattachment',
            name='file',
            field=models.FileField(upload_to=member.models.get_enterprise_attachment_path, verbose_name='\u6587\u4ef6'),
        ),
        migrations.AlterField(
            model_name='enterpriseattachment',
            name='thumbnail',
            field=models.FileField(help_text='\u4ec5\u56fe\u7247\u7c7b\u578b\u6587\u4ef6\u81ea\u52a8\u751f\u6210', upload_to=member.models.get_enterprise_attachment_thumbnail_path, null=True, verbose_name='\u7f29\u7565\u6587\u4ef6', blank=True),
        ),
    ]
