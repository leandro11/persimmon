# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0017_remove_staff_department'),
        ('ticket', '0010_invoice_send_ems'),
    ]

    operations = [
        migrations.CreateModel(
            name='InvoiceLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('before_status', models.CharField(blank=True, max_length=30, null=True, verbose_name='\u53d8\u66f4\u524d\u72b6\u6001', choices=[(b'LODGED', '\u5df2\u5f00\u5177'), (b'FINISHED', '\u5df2\u5bc4\u51fa')])),
                ('after_status', models.CharField(max_length=30, verbose_name='\u53d8\u66f4\u540e\u72b6\u6001', choices=[(b'LODGED', '\u5df2\u5f00\u5177'), (b'FINISHED', '\u5df2\u5bc4\u51fa')])),
                ('remarks', models.CharField(max_length=300, null=True, verbose_name='\u64cd\u4f5c\u72b6\u6001', blank=True)),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('invoice', models.ForeignKey(verbose_name='\u53d1\u7968', to='ticket.Invoice')),
                ('oprator', models.ForeignKey(verbose_name='\u6267\u884c\u4eba', to='management.Staff')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TicketeLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('before_status', models.CharField(max_length=30, verbose_name='\u53d8\u66f4\u524d\u72b6\u6001', choices=[(b'RECEIVED_PENDING', '\u6536\u7968\u5f85\u6838'), (b'RECEIVED', '\u6536\u7968\u5df2\u6838'), (b'VERIFIED_PENDING', '\u9a8c\u7968\u5f85\u6838'), (b'VERIFIED', '\u9a8c\u7968\u5df2\u6838'), (b'ARRIVE_PENDING', '\u5165\u5e93\u5f85\u6838'), (b'ARRIVED', '\u5165\u5e93\u5df2\u6838'), (b'FINISHED_PENDING', '\u51fa\u5e93\u5f85\u6838'), (b'FINISHED', '\u51fa\u5e93\u5df2\u6838')])),
                ('after_status', models.CharField(max_length=30, verbose_name='\u53d8\u66f4\u540e\u72b6\u6001', choices=[(b'RECEIVED_PENDING', '\u6536\u7968\u5f85\u6838'), (b'RECEIVED', '\u6536\u7968\u5df2\u6838'), (b'VERIFIED_PENDING', '\u9a8c\u7968\u5f85\u6838'), (b'VERIFIED', '\u9a8c\u7968\u5df2\u6838'), (b'ARRIVE_PENDING', '\u5165\u5e93\u5f85\u6838'), (b'ARRIVED', '\u5165\u5e93\u5df2\u6838'), (b'FINISHED_PENDING', '\u51fa\u5e93\u5f85\u6838'), (b'FINISHED', '\u51fa\u5e93\u5df2\u6838')])),
                ('remarks', models.CharField(max_length=300, null=True, verbose_name='\u64cd\u4f5c\u72b6\u6001', blank=True)),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('oprator', models.ForeignKey(verbose_name='\u6267\u884c\u4eba', to='management.Staff')),
                ('ticket', models.ForeignKey(verbose_name='\u53d1\u7968', to='ticket.TransactionTicket')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='send_ems',
            field=models.CharField(max_length=50, unique=True, null=True, verbose_name='\u5bc4\u51faEMS', blank=True),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='status',
            field=models.CharField(default=b'LODGED', max_length=30, verbose_name='\u64cd\u4f5c\u72b6\u6001', choices=[(b'LODGED', '\u5df2\u5f00\u5177'), (b'FINISHED', '\u5df2\u5bc4\u51fa')]),
        ),
        migrations.AlterField(
            model_name='transactionticket',
            name='status',
            field=models.CharField(default=b'RECEIVED_PENDING', max_length=30, verbose_name='\u64cd\u4f5c\u72b6\u6001', choices=[(b'RECEIVED_PENDING', '\u6536\u7968\u5f85\u6838'), (b'RECEIVED', '\u6536\u7968\u5df2\u6838'), (b'VERIFIED_PENDING', '\u9a8c\u7968\u5f85\u6838'), (b'VERIFIED', '\u9a8c\u7968\u5df2\u6838'), (b'ARRIVE_PENDING', '\u5165\u5e93\u5f85\u6838'), (b'ARRIVED', '\u5165\u5e93\u5df2\u6838'), (b'FINISHED_PENDING', '\u51fa\u5e93\u5f85\u6838'), (b'FINISHED', '\u51fa\u5e93\u5df2\u6838')]),
        ),
    ]
