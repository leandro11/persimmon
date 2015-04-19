#coding=utf-8

from django.db import models
from django.core import validators
from django.contrib.auth.models import User, UserManager
from django.utils.translation import ugettext_lazy as _
from utils.constants import STAFF_TYPE


class Province(models.Model):
    name = models.CharField(max_length=20, blank=False, null=False, verbose_name=u'省份名称')

    class Meta:
        verbose_name = u'省份'
        verbose_name_plural = u'省份'

    def __unicode__(self):
        return u"%s" % self.name


class Zone(models.Model):
    name = models.CharField(max_length=20, blank=False, null=False, verbose_name=u'区域名称')
    provinces = models.ManyToManyField(Province, blank=False, null=False, verbose_name=u'包含省份')

    class Meta:
        verbose_name = u'区域'
        verbose_name_plural = u'区域划分'

    def __unicode__(self):
        return "%s" % self.name


class Staff(models.Model):
    '''
    工作人员
    '''
    user = models.OneToOneField(User, blank=False, null=False, verbose_name=u'登陆账号')
    name = models.CharField(unique=True, max_length=50, blank=False, null=False, verbose_name=u'姓名', validators=[validators.MinLengthValidator(2), ])
    email = models.CharField(max_length=50, blank=False, null=False, verbose_name=u'邮件地址', validators=[validators.MinLengthValidator(2), ])
    mobile_number = models.CharField(max_length=14, blank=False, null=False, verbose_name=u'手机号',
                                     validators=[validators.RegexValidator(r'^[\d+]+$', _(u'请输入合法的手机号'), 'mobile_invalid'), ])
    telephone = models.CharField(max_length=11, blank=True, null=True, verbose_name=u'固定电话',
                                 validators=[validators.RegexValidator(r'^[\d-]+$', _(u'请输入合法的电话号码'), 'telephone_invalid'), ])
    fax_number = models.CharField(max_length=11, blank=False, null=False, verbose_name=u'传真号',
                                  validators=[validators.RegexValidator(r'^[\d-]+$', _(u'请输入合法的传真号'), 'fax_invalid'), ])
    position = models.CharField(max_length=30, blank=False, null=False, verbose_name=u'职位', help_text=u'必填', choices=STAFF_TYPE)
    zone = models.ManyToManyField(Zone, verbose_name=u'负责区域')

    class Meta:
        verbose_name = u'工作人员'
        verbose_name_plural = u'工作人员'

    def __unicode__(self):
        if self.user.groups.count() > 0:
            return u"[%s]%s" % (self.user.groups.all()[0].name, self.name)
        else:
            return u"[工作人员]%s" % self.name

    @property
    def groupname(self):
        if self.user.groups.count() > 0:
            return self.user.groups.all()[0].name
        else:
            return None

    @property
    def grouptype(self):
        if self.user.groups.count() > 0:
            return self.user.groups.all()[0].id
        else:
            return None

    @property
    def is_contactor(self):
        return False

    @property
    def member_type(self):
        return 'platform'

    @property
    def contactor_id(self):
        return None

    @property
    def username(self):
        return self.user.username
