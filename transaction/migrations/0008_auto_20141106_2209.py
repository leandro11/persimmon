# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0007_auto_20141106_1841'),
    ]

    operations = [
        migrations.AddField(
            model_name='transactionmetaoperation',
            name='need_confirm',
            field=models.BooleanField(default=False, verbose_name='\u9700\u5ba2\u670d\u786e\u8ba4'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='transactiontype',
            name='name',
            field=models.CharField(default=b'CASHIN_5DAY', max_length=20, verbose_name='\u8d34\u73b0\u670d\u52a1\u7c7b\u578b', choices=[(b'CASHIN_2DAY', '\u4e24\u65e5\u8d34\u73b0'), (b'CASHIN_3DAY', '\u4e09\u65e5\u8d34\u73b0'), (b'CASHIN_5DAY', '\u4e94\u65e5\u8d34\u73b0'), (b'CASHIN_7DAY', '\u4e03\u65e5\u8d34\u73b0')]),
        ),
    ]
