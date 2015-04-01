# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0051_auto_20141213_1741'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transactionorder',
            name='ticket_status',
            field=models.CharField(default=b'UNRECEIVED', max_length=30, verbose_name='\u6c47\u7968\u72b6\u6001', choices=[(b'UNRECEIVED', '\u672a\u6536\u7968'), (b'RECEIVED_PENDING', '\u6536\u7968\u5f85\u6838'), (b'RECEIVED', '\u6536\u7968\u5df2\u6838'), (b'VERIFIED_PENDING', '\u9a8c\u7968\u5f85\u6838'), (b'VERIFIED', '\u9a8c\u7968\u5df2\u6838'), (b'CHECKIN_PENDING', '\u5165\u5e93\u5f85\u6838'), (b'CHECKIN', '\u5165\u5e93\u5df2\u6838'), (b'CHECKOUT_PENDING', '\u51fa\u5e93\u5f85\u6838'), (b'CHECKOUT', '\u51fa\u5e93\u5df2\u6838')]),
        ),
    ]
