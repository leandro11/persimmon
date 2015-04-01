# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('member', '0028_auto_20141223_2304'),
    ]

    operations = [
        migrations.CreateModel(
            name='BankAttachment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text='\u6240\u6709\u6a21\u677f\u6587\u6863\u6587\u4ef6\u540d\u4e0d\u53ef\u91cd\u590d', unique=True, max_length=50, verbose_name='\u6587\u4ef6\u540d\u79f0')),
                ('type', models.CharField(max_length=50, verbose_name='\u6587\u4ef6\u7c7b\u578b', choices=[('\u6218\u7565\u5408\u4f5c\u534f\u8bae', '\u6218\u7565\u5408\u4f5c\u534f\u8bae'), ('\u627f\u8bfa\u4e662', '\u627f\u8bfa\u4e662')])),
                ('file', models.FileField(upload_to=b'./bank/', verbose_name='\u6587\u4ef6')),
                ('thumbnail', models.FileField(help_text='\u4ec5\u56fe\u7247\u7c7b\u578b\u6587\u4ef6\u81ea\u52a8\u751f\u6210', upload_to=b'./bank/thumbnail', null=True, verbose_name='\u7f29\u7565\u6587\u4ef6', blank=True)),
                ('extension', models.CharField(max_length=10, verbose_name='\u6269\u5c55\u540d')),
                ('size', models.DecimalField(help_text='\u5355\u4f4dKB', verbose_name='\u6587\u4ef6\u5927\u5c0f', max_digits=10, decimal_places=2)),
                ('width', models.PositiveSmallIntegerField(help_text='\u56fe\u7247\u5bbd\u5ea6\uff0c\u4ec5\u5f53\u6587\u4ef6\u7c7b\u578b\u4e3a\u56fe\u7247\u65f6', max_length=10, null=True, verbose_name='\u5bbd\u5ea6', blank=True)),
                ('height', models.PositiveSmallIntegerField(help_text='\u56fe\u7247\u9ad8\u5ea6\uff0c\u4ec5\u5f53\u6587\u4ef6\u7c7b\u578b\u4e3a\u56fe\u7247\u65f6', max_length=10, null=True, verbose_name='\u9ad8\u5ea6', blank=True)),
                ('need_login', models.BooleanField(default=True, help_text='\u9700\u8981\u767b\u9646\u624d\u80fd\u4e0b\u8f7d', verbose_name='\u9700\u8981\u767b\u9646')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('bank', models.ForeignKey(verbose_name='\u6240\u5c5e\u94f6\u884c', to='member.Bank')),
                ('creator', models.ForeignKey(verbose_name='\u64cd\u4f5c\u7528\u6237', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'verbose_name': '\u94f6\u884c\u4f1a\u5458\u9644\u4ef6',
                'verbose_name_plural': '\u94f6\u884c\u4f1a\u5458\u9644\u4ef6',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EnterpriseAttachment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text='\u6240\u6709\u6a21\u677f\u6587\u6863\u6587\u4ef6\u540d\u4e0d\u53ef\u91cd\u590d', unique=True, max_length=50, verbose_name='\u6587\u4ef6\u540d\u79f0')),
                ('type', models.CharField(max_length=50, verbose_name='\u6587\u4ef6\u7c7b\u578b', choices=[('\u8425\u4e1a\u6267\u7167', '\u8425\u4e1a\u6267\u7167'), ('\u673a\u6784\u4ee3\u7801', '\u673a\u6784\u4ee3\u7801'), ('\u7a0e\u52a1\u767b\u8bb0\u8bc1', '\u7a0e\u52a1\u767b\u8bb0\u8bc1')])),
                ('file', models.FileField(upload_to=b'./enterprise/', verbose_name='\u6587\u4ef6')),
                ('thumbnail', models.FileField(help_text='\u4ec5\u56fe\u7247\u7c7b\u578b\u6587\u4ef6\u81ea\u52a8\u751f\u6210', upload_to=b'./enterprise/thumbnail', null=True, verbose_name='\u7f29\u7565\u6587\u4ef6', blank=True)),
                ('extension', models.CharField(max_length=10, verbose_name='\u6269\u5c55\u540d')),
                ('size', models.DecimalField(help_text='\u5355\u4f4dKB', verbose_name='\u6587\u4ef6\u5927\u5c0f', max_digits=10, decimal_places=2)),
                ('width', models.PositiveSmallIntegerField(help_text='\u56fe\u7247\u5bbd\u5ea6\uff0c\u4ec5\u5f53\u6587\u4ef6\u7c7b\u578b\u4e3a\u56fe\u7247\u65f6', max_length=10, null=True, verbose_name='\u5bbd\u5ea6', blank=True)),
                ('height', models.PositiveSmallIntegerField(help_text='\u56fe\u7247\u9ad8\u5ea6\uff0c\u4ec5\u5f53\u6587\u4ef6\u7c7b\u578b\u4e3a\u56fe\u7247\u65f6', max_length=10, null=True, verbose_name='\u9ad8\u5ea6', blank=True)),
                ('need_login', models.BooleanField(default=True, help_text='\u9700\u8981\u767b\u9646\u624d\u80fd\u4e0b\u8f7d', verbose_name='\u9700\u8981\u767b\u9646')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('creator', models.ForeignKey(verbose_name='\u64cd\u4f5c\u7528\u6237', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('enterprise', models.ForeignKey(verbose_name='\u6240\u5c5e\u4f01\u4e1a', to='member.Enterprise')),
            ],
            options={
                'verbose_name': '\u4f01\u4e1a\u4f1a\u5458\u9644\u4ef6',
                'verbose_name_plural': '\u4f01\u4e1a\u4f1a\u5458\u9644\u4ef6',
            },
            bases=(models.Model,),
        ),
    ]
