# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0010_auto_20141111_2344'),
    ]

    operations = [
        migrations.AddField(
            model_name='bank',
            name='level',
            field=models.CharField(default=b'1', max_length=20, verbose_name='\u4f1a\u5458\u661f\u7ea7', choices=[(b'1', '\u4e00\u661f\u4f1a\u5458'), (b'2', '\u4e8c\u661f\u4f1a\u5458'), (b'3', '\u4e09\u661f\u4f1a\u5458'), (b'4', '\u56db\u661f\u4f1a\u5458'), (b'5', '\u4e94\u661f\u4f1a\u5458'), (b'6', '\u516d\u661f\u4f1a\u5458')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='enterprise',
            name='level',
            field=models.CharField(default=b'1', max_length=20, verbose_name='\u4f1a\u5458\u661f\u7ea7', choices=[(b'1', '\u4e00\u661f\u4f1a\u5458'), (b'2', '\u4e8c\u661f\u4f1a\u5458'), (b'3', '\u4e09\u661f\u4f1a\u5458'), (b'4', '\u56db\u661f\u4f1a\u5458'), (b'5', '\u4e94\u661f\u4f1a\u5458'), (b'6', '\u516d\u661f\u4f1a\u5458')]),
            preserve_default=True,
        ),
    ]
