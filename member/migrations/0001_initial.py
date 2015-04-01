# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Bank',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=50, verbose_name='\u94f6\u884c\u5168\u79f0', validators=[django.core.validators.MinLengthValidator(2)])),
                ('short_name', models.CharField(max_length=20, verbose_name='\u94f6\u884c\u7b80\u79f0', validators=[django.core.validators.MinLengthValidator(2)])),
                ('city', models.CharField(max_length=20, verbose_name='\u57ce\u5e02')),
                ('address', models.CharField(max_length=100, verbose_name='\u5730\u5740')),
                ('zipcode', models.IntegerField(verbose_name='\u90ae\u7f16')),
                ('fax_number', models.IntegerField(max_length=20, verbose_name='\u4f20\u771f\u53f7', validators=[django.core.validators.MinValueValidator(100000)])),
                ('strategic_agreements', models.ImageField(max_length=200, upload_to=b'/', null=True, verbose_name='\u6218\u7565\u5408\u4f5c\u534f\u8bae', blank=True)),
                ('execution_agreements', models.ImageField(max_length=200, upload_to=b'/', null=True, verbose_name='\u6267\u884c\u5408\u4f5c\u534f\u8bae', blank=True)),
                ('status', models.CharField(default=b'Pending', max_length=20, verbose_name='\u4f1a\u5458\u72b6\u6001', choices=[(b'Enabled', '\u6b63\u5e38'), (b'Pending', '\u5f85\u5ba1\u6838'), (b'Disabled', '\u7981\u7528'), (b'Expired', '\u8fc7\u671f')])),
                ('expired_date', models.DateTimeField(null=True, verbose_name='\u5408\u4f5c\u8fc7\u671f\u65f6\u95f4')),
                ('create_date', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('modify_date', models.DateTimeField(auto_now=True, verbose_name='\u6700\u540e\u4fee\u6539\u65f6\u95f4', auto_now_add=True)),
            ],
            options={
                'verbose_name': '\u94f6\u884c\u4f1a\u5458',
                'verbose_name_plural': '\u94f6\u884c\u4f1a\u5458',
                'permissions': (('register_bank', '\u6ce8\u518c\u94f6\u884c\u4f1a\u5458'),),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='BankContactor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('username', models.CharField(help_text='\u957f\u5ea6\u5c0f\u4e8e30\uff0c\u53ea\u9650\u5b57\u6bcd\u3001\u6570\u5b57\u53ca\u7b26\u53f7@.+-_', unique=True, max_length=30, verbose_name='\u7528\u6237\u540d')),
                ('groupname', models.CharField(choices=[('\u94f6\u884c\u4f1a\u5458\u4e3b\u8054\u7edc\u4eba', '\u94f6\u884c\u4f1a\u5458\u4e3b\u8054\u7edc\u4eba'), ('\u94f6\u884c\u4f1a\u5458\u6267\u884c\u4eba', '\u94f6\u884c\u4f1a\u5458\u6267\u884c\u4eba'), ('\u4f01\u4e1a\u4f1a\u5458\u4e3b\u8054\u7edc\u4eba', '\u4f01\u4e1a\u4f1a\u5458\u4e3b\u8054\u7edc\u4eba'), ('\u4f01\u4e1a\u4f1a\u5458\u6267\u884c\u4eba', '\u4f01\u4e1a\u4f1a\u5458\u6267\u884c\u4eba')], max_length=20, blank=True, help_text='\u89d2\u8272\u540d\u79f0', null=True, verbose_name='\u89d2\u8272\u540d\u79f0')),
                ('name', models.CharField(max_length=50, verbose_name='\u59d3\u540d')),
                ('identity_card', models.CharField(max_length=20, verbose_name='\u8eab\u4efd\u8bc1')),
                ('mobile_number', models.BigIntegerField(max_length=15, verbose_name='\u624b\u673a\u53f7')),
                ('telephone', models.BigIntegerField(max_length=11, null=True, verbose_name='\u56fa\u5b9a\u7535\u8bdd', blank=True)),
                ('email', models.EmailField(max_length=50, verbose_name='\u7535\u5b50\u90ae\u7bb1')),
                ('fax_number', models.BigIntegerField(max_length=20, null=True, verbose_name='\u4f20\u771f\u53f7', blank=True)),
                ('position', models.CharField(max_length=20, null=True, verbose_name='\u804c\u4f4d', blank=True)),
                ('pwd_question', models.CharField(max_length=100, verbose_name='\u5bc6\u7801\u63d0\u793a\u95ee\u9898')),
                ('pwd_answer', models.CharField(max_length=50, verbose_name='\u5bc6\u7801\u63d0\u793a\u95ee\u9898\u7b54\u6848')),
                ('create_date', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('modify_date', models.DateTimeField(auto_now=True, verbose_name='\u6700\u540e\u4fee\u6539\u65f6\u95f4', auto_now_add=True)),
                ('bank', models.OneToOneField(verbose_name='\u6240\u5c5e\u94f6\u884c', to='member.Bank')),
                ('user', models.OneToOneField(verbose_name='\u767b\u9646\u8d26\u53f7', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '\u94f6\u884c\u4f1a\u5458\u4e3b\u8054\u7edc\u4eba',
                'verbose_name_plural': '\u94f6\u884c\u4f1a\u5458\u4e3b\u8054\u7edc\u4eba',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='BankOperator',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('username', models.CharField(help_text='\u957f\u5ea6\u5c0f\u4e8e30\uff0c\u53ea\u9650\u5b57\u6bcd\u3001\u6570\u5b57\u53ca\u7b26\u53f7@.+-_', unique=True, max_length=30, verbose_name='\u7528\u6237\u540d')),
                ('groupname', models.CharField(choices=[('\u94f6\u884c\u4f1a\u5458\u4e3b\u8054\u7edc\u4eba', '\u94f6\u884c\u4f1a\u5458\u4e3b\u8054\u7edc\u4eba'), ('\u94f6\u884c\u4f1a\u5458\u6267\u884c\u4eba', '\u94f6\u884c\u4f1a\u5458\u6267\u884c\u4eba'), ('\u4f01\u4e1a\u4f1a\u5458\u4e3b\u8054\u7edc\u4eba', '\u4f01\u4e1a\u4f1a\u5458\u4e3b\u8054\u7edc\u4eba'), ('\u4f01\u4e1a\u4f1a\u5458\u6267\u884c\u4eba', '\u4f01\u4e1a\u4f1a\u5458\u6267\u884c\u4eba')], max_length=20, blank=True, help_text='\u89d2\u8272\u540d\u79f0', null=True, verbose_name='\u89d2\u8272\u540d\u79f0')),
                ('name', models.CharField(max_length=50, verbose_name='\u59d3\u540d')),
                ('identity_card', models.CharField(max_length=20, verbose_name='\u8eab\u4efd\u8bc1')),
                ('mobile_number', models.BigIntegerField(max_length=11, verbose_name='\u624b\u673a\u53f7')),
                ('telephone', models.BigIntegerField(max_length=11, null=True, verbose_name='\u56fa\u5b9a\u7535\u8bdd', blank=True)),
                ('email', models.EmailField(max_length=50, verbose_name='\u7535\u5b50\u90ae\u7bb1')),
                ('fax_number', models.BigIntegerField(max_length=11, null=True, verbose_name='\u4f20\u771f\u53f7', blank=True)),
                ('position', models.CharField(max_length=20, null=True, verbose_name='\u804c\u4f4d', blank=True)),
                ('pwd_question', models.CharField(max_length=100, null=True, verbose_name='\u5bc6\u7801\u63d0\u793a\u95ee\u9898', blank=True)),
                ('pwd_answer', models.CharField(max_length=50, null=True, verbose_name='\u5bc6\u7801\u63d0\u793a\u95ee\u9898\u7b54\u6848', blank=True)),
                ('create_date', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('modify_date', models.DateTimeField(auto_now=True, verbose_name='\u6700\u540e\u4fee\u6539\u65f6\u95f4', auto_now_add=True)),
                ('bank', models.ForeignKey(verbose_name='\u6240\u5c5e\u94f6\u884c', to='member.Bank')),
                ('user', models.OneToOneField(null=True, blank=True, to=settings.AUTH_USER_MODEL, verbose_name='\u767b\u9646\u8d26\u53f7')),
            ],
            options={
                'verbose_name': '\u94f6\u884c\u4f1a\u5458\u6267\u884c\u4eba',
                'verbose_name_plural': '\u94f6\u884c\u4f1a\u5458\u6267\u884c\u4eba',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Enterprise',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=50, verbose_name='\u4f01\u4e1a\u540d\u79f0')),
                ('city', models.CharField(max_length=20, verbose_name='\u57ce\u5e02')),
                ('address', models.CharField(max_length=100, verbose_name='\u5730\u5740')),
                ('zipcode', models.IntegerField(verbose_name='\u90ae\u7f16')),
                ('fax_number', models.IntegerField(verbose_name='\u4f20\u771f\u53f7')),
                ('licence', models.ImageField(max_length=200, upload_to=b'/', null=True, verbose_name='\u8425\u4e1a\u6267\u7167', blank=True)),
                ('status', models.CharField(default=b'Pending', max_length=20, verbose_name='\u4f1a\u5458\u72b6\u6001', choices=[(b'Enabled', '\u6b63\u5e38'), (b'Pending', '\u5f85\u5ba1\u6838'), (b'Disabled', '\u7981\u7528'), (b'Expired', '\u8fc7\u671f')])),
                ('create_date', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('modify_date', models.DateTimeField(auto_now=True, verbose_name='\u6700\u540e\u4fee\u6539\u65f6\u95f4', auto_now_add=True)),
            ],
            options={
                'verbose_name': '\u4f01\u4e1a\u4f1a\u5458',
                'verbose_name_plural': '\u4f01\u4e1a\u4f1a\u5458',
                'permissions': (('register_enterprise', '\u6ce8\u518c\u4f01\u4e1a\u4f1a\u5458'),),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EnterpriseContactor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('username', models.CharField(help_text='\u957f\u5ea6\u5c0f\u4e8e30\uff0c\u53ea\u9650\u5b57\u6bcd\u3001\u6570\u5b57\u53ca\u7b26\u53f7@.+-_', unique=True, max_length=30, verbose_name='\u7528\u6237\u540d')),
                ('groupname', models.CharField(choices=[('\u94f6\u884c\u4f1a\u5458\u4e3b\u8054\u7edc\u4eba', '\u94f6\u884c\u4f1a\u5458\u4e3b\u8054\u7edc\u4eba'), ('\u94f6\u884c\u4f1a\u5458\u6267\u884c\u4eba', '\u94f6\u884c\u4f1a\u5458\u6267\u884c\u4eba'), ('\u4f01\u4e1a\u4f1a\u5458\u4e3b\u8054\u7edc\u4eba', '\u4f01\u4e1a\u4f1a\u5458\u4e3b\u8054\u7edc\u4eba'), ('\u4f01\u4e1a\u4f1a\u5458\u6267\u884c\u4eba', '\u4f01\u4e1a\u4f1a\u5458\u6267\u884c\u4eba')], max_length=20, blank=True, help_text='\u89d2\u8272\u540d\u79f0', null=True, verbose_name='\u89d2\u8272\u540d\u79f0')),
                ('name', models.CharField(max_length=50, verbose_name='\u59d3\u540d')),
                ('identity_card', models.CharField(max_length=20, verbose_name='\u8eab\u4efd\u8bc1')),
                ('mobile_number', models.BigIntegerField(max_length=11, verbose_name='\u624b\u673a\u53f7')),
                ('telephone', models.BigIntegerField(max_length=11, null=True, verbose_name='\u56fa\u5b9a\u7535\u8bdd', blank=True)),
                ('email', models.EmailField(max_length=50, verbose_name='\u7535\u5b50\u90ae\u7bb1')),
                ('fax_number', models.BigIntegerField(max_length=11, null=True, verbose_name='\u4f20\u771f\u53f7', blank=True)),
                ('position', models.CharField(max_length=20, null=True, verbose_name='\u804c\u4f4d', blank=True)),
                ('pwd_question', models.CharField(max_length=100, verbose_name='\u5bc6\u7801\u63d0\u793a\u95ee\u9898')),
                ('pwd_answer', models.CharField(max_length=50, verbose_name='\u5bc6\u7801\u63d0\u793a\u95ee\u9898\u7b54\u6848')),
                ('create_date', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('modify_date', models.DateTimeField(auto_now=True, verbose_name='\u6700\u540e\u4fee\u6539\u65f6\u95f4', auto_now_add=True)),
                ('enterprise', models.OneToOneField(verbose_name='\u6240\u5c5e\u4f01\u4e1a', to='member.Enterprise')),
                ('user', models.OneToOneField(null=True, blank=True, to=settings.AUTH_USER_MODEL, verbose_name='\u767b\u9646\u8d26\u53f7')),
            ],
            options={
                'verbose_name': '\u4f01\u4e1a\u4f1a\u5458\u4e3b\u8054\u7edc\u4eba',
                'verbose_name_plural': '\u4f01\u4e1a\u4f1a\u5458\u4e3b\u8054\u7edc\u4eba',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EnterpriseOperator',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('username', models.CharField(help_text='\u957f\u5ea6\u5c0f\u4e8e30\uff0c\u53ea\u9650\u5b57\u6bcd\u3001\u6570\u5b57\u53ca\u7b26\u53f7@.+-_', unique=True, max_length=30, verbose_name='\u7528\u6237\u540d')),
                ('groupname', models.CharField(choices=[('\u94f6\u884c\u4f1a\u5458\u4e3b\u8054\u7edc\u4eba', '\u94f6\u884c\u4f1a\u5458\u4e3b\u8054\u7edc\u4eba'), ('\u94f6\u884c\u4f1a\u5458\u6267\u884c\u4eba', '\u94f6\u884c\u4f1a\u5458\u6267\u884c\u4eba'), ('\u4f01\u4e1a\u4f1a\u5458\u4e3b\u8054\u7edc\u4eba', '\u4f01\u4e1a\u4f1a\u5458\u4e3b\u8054\u7edc\u4eba'), ('\u4f01\u4e1a\u4f1a\u5458\u6267\u884c\u4eba', '\u4f01\u4e1a\u4f1a\u5458\u6267\u884c\u4eba')], max_length=20, blank=True, help_text='\u89d2\u8272\u540d\u79f0', null=True, verbose_name='\u89d2\u8272\u540d\u79f0')),
                ('name', models.CharField(max_length=50, verbose_name='\u59d3\u540d')),
                ('identity_card', models.CharField(max_length=20, verbose_name='\u8eab\u4efd\u8bc1')),
                ('mobile_number', models.BigIntegerField(max_length=11, verbose_name='\u624b\u673a\u53f7')),
                ('telephone', models.BigIntegerField(max_length=11, null=True, verbose_name='\u56fa\u5b9a\u7535\u8bdd', blank=True)),
                ('email', models.EmailField(max_length=50, verbose_name='\u7535\u5b50\u90ae\u7bb1')),
                ('fax_number', models.BigIntegerField(max_length=11, null=True, verbose_name='\u4f20\u771f\u53f7', blank=True)),
                ('position', models.CharField(max_length=20, null=True, verbose_name='\u804c\u4f4d', blank=True)),
                ('pwd_question', models.CharField(max_length=100, null=True, verbose_name='\u5bc6\u7801\u63d0\u793a\u95ee\u9898', blank=True)),
                ('pwd_answer', models.CharField(max_length=50, null=True, verbose_name='\u5bc6\u7801\u63d0\u793a\u95ee\u9898\u7b54\u6848', blank=True)),
                ('create_date', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('modify_date', models.DateTimeField(auto_now=True, verbose_name='\u6700\u540e\u4fee\u6539\u65f6\u95f4', auto_now_add=True)),
                ('enterprise', models.ForeignKey(verbose_name='\u6240\u5c5e\u4f01\u4e1a', to='member.Enterprise')),
                ('user', models.OneToOneField(verbose_name='\u767b\u9646\u8d26\u53f7', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '\u4f01\u4e1a\u4f1a\u5458\u6267\u884c\u4eba',
                'verbose_name_plural': '\u4f01\u4e1a\u4f1a\u5458\u6267\u884c\u4eba',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RegisterInvitationCode',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(unique=True, max_length=30, verbose_name='\u9080\u8bf7\u7801')),
                ('member_name', models.CharField(help_text='\u8bf7\u586b\u5199\u9080\u8bf7\u4f1a\u5458\u5355\u4f4d\u540d\u79f0', max_length=50, verbose_name='\u4f1a\u5458\u5355\u4f4d\u540d\u79f0')),
                ('member_type', models.CharField(max_length=20, verbose_name='\u4f1a\u5458\u7c7b\u578b', choices=[(b'Bank', '\u94f6\u884c\u4f1a\u5458'), (b'Enterprise', '\u4f01\u4e1a\u4f1a\u5458')])),
                ('status', models.CharField(default=b'Activated', max_length=10, verbose_name='\u9080\u8bf7\u7801\u72b6\u6001', choices=[(b'Activated', '\u672a\u4f7f\u7528'), (b'Used', '\u5df2\u4f7f\u7528'), (b'Inactived', '\u5df2\u4f5c\u5e9f')])),
                ('used_date', models.DateTimeField(null=True, verbose_name='\u4f7f\u7528\u65f6\u95f4', blank=True)),
                ('create_date', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('operator', models.ForeignKey(verbose_name='\u521b\u5efa\u4eba\u5458', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'verbose_name': '\u6ce8\u518c\u9080\u8bf7\u7801',
                'verbose_name_plural': '\u6ce8\u518c\u9080\u8bf7\u7801',
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='enterpriseoperator',
            unique_together=set([('user', 'enterprise')]),
        ),
        migrations.AlterUniqueTogether(
            name='enterprisecontactor',
            unique_together=set([('user', 'enterprise')]),
        ),
        migrations.AddField(
            model_name='enterprise',
            name='invite_code',
            field=models.OneToOneField(verbose_name='\u9080\u8bf7\u7801', to='member.RegisterInvitationCode'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='enterprise',
            name='province',
            field=models.ForeignKey(verbose_name='\u7701\u4efd', to='management.Province'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='bankoperator',
            unique_together=set([('user', 'bank')]),
        ),
        migrations.AlterUniqueTogether(
            name='bankcontactor',
            unique_together=set([('user', 'bank')]),
        ),
        migrations.AddField(
            model_name='bank',
            name='invite_code',
            field=models.OneToOneField(verbose_name='\u9080\u8bf7\u7801', to='member.RegisterInvitationCode'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='bank',
            name='province',
            field=models.ForeignKey(verbose_name='\u7701\u4efd', to='management.Province'),
            preserve_default=True,
        ),
    ]
