# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import utils.models


class Migration(migrations.Migration):

    dependencies = [
        ('utils', '0010_auto_20141226_1654'),
    ]

    operations = [
        migrations.AlterField(
            model_name='templateattachment',
            name='file',
            field=models.FileField(upload_to=utils.models.get_template_attachment_path, verbose_name='\u6587\u4ef6'),
        ),
    ]
