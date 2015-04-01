# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0005_auto_20141112_1009'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transactionticket',
            name='status',
            field=models.CharField(default=b'RECEIVED', max_length=30, verbose_name='\u64cd\u4f5c\u72b6\u6001', choices=[(b'RECEIVED', '\u5df2\u6536\u7968'), (b'VERIFIED', '\u5df2\u9a8c\u7968'), (b'ARRIVED', '\u5df2\u5165\u5e93'), (b'PENDING', '\u5f85\u5ba1\u6838'), (b'FINISHED', '\u5df2\u51fa\u5e93'), (b'FINISHED', '\u5df2\u4f5c\u5e9f')]),
        ),
    ]
