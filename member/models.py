#coding=utf-8

from django.db import models
from management.models import Province
from django.contrib.auth.models import User, UserManager
from django.db.models.signals import *
from django.core import validators
from utils.constants import MEMBER_USER_TYPE
from management.models import Staff
from TTMS.settings import MEDIA_URL, MEDIA_ROOT, BASE_URL
from django.utils.http import urlquote
from PIL import Image
import os
from utils.func import make_thumb
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _


module = __name__[:__name__.find('.')]

#=====================================================注册邀请码======================================================

CODE_PENDING = 'PENDING'
CODE_ACTIVATED = 'Activated'
CODE_USED = 'Used'
CODE_INACTIVED = 'Inactived'
CODE_STATUS = (
    (CODE_PENDING, u'待审核'),
    (CODE_ACTIVATED, u'未使用'),
    (CODE_USED, u'已使用'),
    (CODE_INACTIVED, u'已作废'),
)

BANK_MEMBER = 'Bank'
ENTERPRISE_MEMBER = 'Enterprise'
MEMBER_TYPE = (
    (BANK_MEMBER, u'银行会员'),
    (ENTERPRISE_MEMBER, u'企业会员'),
)


class RegisterInvitationCode(models.Model):
    code = models.CharField(unique=True, max_length=30, blank=False, null=False, verbose_name=u'邀请码')
    member_name = models.CharField(max_length=50, blank=False, null=False, verbose_name=u'会员名称')
    member_type = models.CharField(max_length=20, choices=MEMBER_TYPE, verbose_name=u'会员类型')
    contactor_name = models.CharField(max_length=20, blank=False, null=False, verbose_name=u'主联络人姓名')
    contactor_email = models.EmailField(max_length=50, blank=False, null=False, verbose_name=u'主联络人邮箱')
    referee_member_type = models.CharField(max_length=20, blank=True, null=True, choices=MEMBER_TYPE, verbose_name=u'推荐会员类型')
    referee_member_id = models.BigIntegerField(blank=True, null=True, verbose_name=u'推荐会员编号')
    status = models.CharField(max_length=10, choices=CODE_STATUS, default=CODE_ACTIVATED, verbose_name=u'邀请码状态')
    market_manager = models.ForeignKey(Staff, blank=True, null=True, verbose_name=u'市场经理')
    used_date = models.DateTimeField(blank=True, null=True, editable=True, verbose_name=u'使用时间')
    create_date = models.DateTimeField(auto_now_add=True, editable=True, verbose_name=u'创建时间')

    class Meta:
        verbose_name = u'注册邀请码'
        verbose_name_plural = u'注册邀请码'

    def __unicode__(self):
        return u'[邀请码]%s' % self.code

    def get_referee(self):
        if self.referee_member_type == BANK_MEMBER:
            return Bank.objects.get(id=self.referee_member_id)
        elif self.referee_member_type == ENTERPRISE_MEMBER:
            return Enterprise.objects.get(id=self.referee_member_id)
        else:
            return None

    def get_referee_name(self):
        if self.referee_member_type == BANK_MEMBER:
            referee = Bank.objects.get(id=self.referee_member_id)
            return u'[银行会员]%s' % referee.name
        elif self.referee_member_type == ENTERPRISE_MEMBER:
            referee = Enterprise.objects.get(id=self.referee_member_id)
            return u'[企业会员]%s' % referee.name
        else:
            return None

    @property
    def url(self):
        return '%s/member/%s/register?code=%s' % (BASE_URL, self.member_type.lower(), self.code)


#=====================================================会员单位======================================================

MEMBER_ENABLED = 'Enabled'
MEMBER_PENDING = 'Pending'
MEMBER_DISABLED = 'Disabled'
MEMBER_EXPIRED = 'Expired'

MEMBER_STATUS = (
    (MEMBER_ENABLED, u'正常'),
    (MEMBER_PENDING, u'待审核'),
    (MEMBER_DISABLED, u'禁用'),
    (MEMBER_EXPIRED, u'过期'),
)

MEMBER_LEVEL_1 = '1'
MEMBER_LEVEL_2 = '2'
MEMBER_LEVEL_3 = '3'
MEMBER_LEVEL_4 = '4'
MEMBER_LEVEL_5 = '5'
MEMBER_LEVEL_6 = '6'
MEMBER_LEVEL = (
    (MEMBER_LEVEL_1, u'一星会员'),
    (MEMBER_LEVEL_2, u'二星会员'),
    (MEMBER_LEVEL_3, u'三星会员'),
    (MEMBER_LEVEL_4, u'四星会员'),
    (MEMBER_LEVEL_5, u'五星会员'),
    (MEMBER_LEVEL_6, u'六星会员'),
)


class Enterprise(models.Model):
    name = models.CharField(unique=True, max_length=50, blank=False, null=False, verbose_name=u'企业名称')
    province = models.ForeignKey(Province, verbose_name=u'省份')
    city = models.CharField(max_length=20, blank=False, null=False, verbose_name=u'城市')
    address = models.CharField(max_length=100, blank=False, null=False, verbose_name=u'地址')
    zipcode = models.IntegerField(blank=False, null=False, verbose_name=u'邮编')
    fax_number = models.IntegerField(blank=False, null=False, verbose_name=u'传真号')
    # licence = models.ImageField(upload_to='.', blank=True, null=True, verbose_name=u'营业执照')
    # organization_code = models.ImageField(upload_to='.', blank=True, null=True, verbose_name=u'组织代码证')
    # tax_registration = models.ImageField(upload_to='.', blank=True, null=True, verbose_name=u'税务登记证')
    level = models.CharField(max_length=20, choices=MEMBER_LEVEL, default=MEMBER_LEVEL_1, verbose_name=u'会员星级')
    # contactor = models.ForeignKey(EnterpriseContactor, verbose_name=u'主联络人')
    # operator = models.ForeignKey(EnterpriseOperator, verbose_name=u'执行人')
    status = models.CharField(max_length=20, choices=MEMBER_STATUS, default=MEMBER_PENDING, verbose_name=u'会员状态')
    invite_code = models.OneToOneField(RegisterInvitationCode, blank=True, null=True, verbose_name=u'邀请码')
    referee_manager = models.ForeignKey(Staff, blank=True, null=True, verbose_name=u'推荐市场经理', related_name='enterprise_referee_manager')
    service_manager = models.ForeignKey(Staff, blank=True, null=True, verbose_name=u'服务市场经理', related_name='enterprise_service_manager')
    reference_count = models.IntegerField(blank=False, null=False, default=0, verbose_name=u'成功推荐注册数')
    create_date = models.DateTimeField(auto_now_add=True, editable=True, verbose_name=u'注册时间')
    modify_date = models.DateTimeField(auto_now_add=True, auto_now=True, editable=True, verbose_name=u'最后修改时间')

    class Meta:
        verbose_name = u'企业会员'
        verbose_name_plural = u'企业会员'
        permissions = (("register_enterprise", u"注册企业会员"),)

    def __unicode__(self):
        return self.name

    def confirm_name_link(self):
        return u'<a href="/staff/member/enterprise/%s/confirm">%s</a>' % (self.id, self.name)

    confirm_name_link.allow_tags = True
    confirm_name_link.short_description = u'企业名称'

    def confirm_button_link(self):
        return u'<a class="button" href="/staff/member/enterprise/%s/confirm">进行审核</a>' % self.id

    confirm_button_link.allow_tags = True
    confirm_button_link.short_description = u'注册审核'


class EnterpriseContactor(models.Model):
    user = models.OneToOneField(User, blank=True, null=True, verbose_name=u'登陆账号')
    enterprise = models.OneToOneField(Enterprise, blank=False, null=False, verbose_name=u'所属企业', related_name='contactor')
    username = models.CharField(unique=True, max_length=30, blank=False, null=False, verbose_name=u'用户名', help_text=u'长度小于30，只限字母、数字及符号@.+-_')
    #groupname = models.CharField(max_length=20, blank=True, null=True, choices=MEMBER_USER_TYPE, verbose_name=u'角色名称', help_text=u'角色名称')
    # password = models.CharField(max_length=20, blank=False, null=False, verbose_name=u'密码')
    name = models.CharField(max_length=50, blank=False, null=False, verbose_name=u'姓名')
    identity_card = models.CharField(max_length=20, blank=False, null=False, verbose_name=u'身份证')
    mobile_number = models.BigIntegerField(max_length=11, blank=False, null=False, verbose_name=u'手机号')
    telephone = models.BigIntegerField(max_length=11, blank=True, null=True, verbose_name=u'固定电话')
    email = models.EmailField(max_length=50, blank=False, null=False, verbose_name=u'电子邮箱')
    # fax_number = models.BigIntegerField(max_length=11, blank=True, null=True, verbose_name=u'传真号')
    position = models.CharField(max_length=20, blank=True, null=True, verbose_name=u'职位')
    pwd_question = models.CharField(max_length=100, blank=False, null=False, verbose_name=u'密码提示问题')
    pwd_answer = models.CharField(max_length=50, blank=False, null=False, verbose_name=u'密码提示问题答案')
    last_login = models.DateTimeField(blank=True, null=True, editable=False, verbose_name=u'上次登录时间')
    create_date = models.DateTimeField(auto_now_add=True, editable=True, verbose_name=u'创建时间')
    modify_date = models.DateTimeField(auto_now_add=True, auto_now=True, editable=True, verbose_name=u'最后修改时间')

    class Meta:
        verbose_name = u'企业会员主联络人'
        verbose_name_plural = u'企业会员主联络人'
        unique_together = (('user', 'enterprise'),)

    def __unicode__(self):
        return u'[%s主联络人]%s' % (self.enterprise.name, self.name)

    @property
    def groupname(self):
        if self.user.groups.count() > 0:
            return self.user.groups.all()[0].name
        else:
            return None

    @property
    def is_contactor(self):
        return True

    @property
    def member_type(self):
        return 'enterprise'

    @property
    def contactor_id(self):
        return self.id

    @property
    def member_id(self):
        return self.enterprise_id

        # @property
        # def username(self):
        #     return self.user.username


class EnterpriseOperator(models.Model):
    user = models.OneToOneField(User, blank=False, null=False, verbose_name=u'登陆账号')
    enterprise = models.OneToOneField(Enterprise, blank=False, null=False, verbose_name=u'所属企业', related_name='operator')  # 企业只能有一个执行人 one to one
    username = models.CharField(unique=True, max_length=30, blank=False, null=False, verbose_name=u'用户名', help_text=u'长度小于30，只限字母、数字及符号@.+-_')
    # groupname = models.CharField(max_length=20, blank=True, null=True, choices=MEMBER_USER_TYPE, verbose_name=u'角色名称', help_text=u'角色名称')
    name = models.CharField(max_length=50, blank=False, null=False, verbose_name=u'姓名')
    identity_card = models.CharField(max_length=20, blank=False, null=False, verbose_name=u'身份证')
    mobile_number = models.BigIntegerField(max_length=11, blank=False, null=False, verbose_name=u'手机号')
    telephone = models.BigIntegerField(max_length=11, blank=True, null=True, verbose_name=u'固定电话')
    email = models.EmailField(max_length=50, blank=False, null=False, verbose_name=u'电子邮箱')
    # fax_number = models.BigIntegerField(max_length=11, blank=True, null=True, verbose_name=u'传真号')
    position = models.CharField(max_length=20, blank=True, null=True, verbose_name=u'职位')
    pwd_question = models.CharField(max_length=100, blank=True, null=True, verbose_name=u'密码提示问题')
    pwd_answer = models.CharField(max_length=50, blank=True, null=True, verbose_name=u'密码提示问题答案')
    last_login = models.DateTimeField(blank=True, null=True, editable=False, verbose_name=u'上次登录时间')
    create_date = models.DateTimeField(auto_now_add=True, editable=True, verbose_name=u'创建时间')
    modify_date = models.DateTimeField(auto_now_add=True, auto_now=True, editable=True, verbose_name=u'最后修改时间')

    class Meta:
        verbose_name = u'企业会员执行人'
        verbose_name_plural = u'企业会员执行人'
        unique_together = (('user', 'enterprise'),)

    def __unicode__(self):
        return u'[%s执行人]%s' % (self.enterprise.name, self.name)

    @property
    def groupname(self):
        if self.user.groups.count() > 0:
            return self.user.groups.all()[0].name
        else:
            return None

    @property
    def is_contactor(self):
        return False

    @property
    def member_type(self):
        return 'enterprise'

    @property
    def contactor_id(self):
        return self.enterprise.contactor.id

    @property
    def member_id(self):
        return self.enterprise_id


class Bank(models.Model):
    '''
    银行会员
    '''
    name = models.CharField(unique=True, max_length=50, blank=False, null=False, verbose_name=u'银行全称', validators=[validators.MinLengthValidator(2), ])
    short_name = models.CharField(unique=True, max_length=20, blank=False, null=False, verbose_name=u'银行简称', validators=[validators.MinLengthValidator(2), ])
    province = models.ForeignKey(Province, verbose_name=u'省份')
    city = models.CharField(max_length=20, blank=False, null=False, verbose_name=u'城市')
    address = models.CharField(max_length=100, blank=False, null=False, verbose_name=u'地址')
    zipcode = models.IntegerField(blank=False, null=False, verbose_name=u'邮编')
    fax_number = models.IntegerField(max_length=20, blank=False, null=False, verbose_name=u'传真号', validators=[validators.MinValueValidator(0), ])
    # licence = models.ImageField(upload_to='.', max_length=200, blank=False, null=False, verbose_name=u'营业执照')
    # strategic_agreements = models.ImageField(upload_to='./bank/', max_length=200, blank=True, null=True, verbose_name=u'战略合作协议')
    # execution_agreements = models.ImageField(upload_to='./bank/', max_length=200, blank=True, null=True, verbose_name=u'执行合作协议')
    level = models.CharField(max_length=20, choices=MEMBER_LEVEL, default=MEMBER_LEVEL_1, verbose_name=u'会员星级')
    # contactor = models.ForeignKey(BankContactor, verbose_name=u'主联络人')
    status = models.CharField(max_length=20, choices=MEMBER_STATUS, default='Pending', verbose_name=u'会员状态')
    invite_code = models.OneToOneField(RegisterInvitationCode, blank=False, null=False, verbose_name=u'邀请码')
    referee_manager = models.ForeignKey(Staff, blank=True, null=True, verbose_name=u'推荐市场经理', related_name='bank_referee_manager')
    service_manager = models.ForeignKey(Staff, blank=True, null=True, verbose_name=u'服务市场经理', related_name='bank_service_manager')
    reference_count = models.IntegerField(blank=False, null=False, default=0, verbose_name=u'成功推荐会员数')
    expired_date = models.DateTimeField(blank=False, null=True, editable=True, verbose_name=u'合作截止时间')
    create_date = models.DateTimeField(auto_now_add=True, editable=True, verbose_name=u'注册时间')
    modify_date = models.DateTimeField(auto_now_add=True, auto_now=True, editable=True, verbose_name=u'最后修改时间')

    class Meta:
        verbose_name = u'银行会员'
        verbose_name_plural = u'银行会员'
        permissions = (("register_bank", u"注册银行会员"),)

    def __unicode__(self):
        return self.name

    def confirm_name_link(self):
        return u'<a href="/staff/member/bank/%s/confirm">%s</a>' % (self.id, self.name)

    confirm_name_link.allow_tags = True
    confirm_name_link.short_description = u'企业名称'

    def confirm_button_link(self):
        return u'<a class="button" href="/staff/member/bank/%s/confirm">进行审核</a>' % self.id

    confirm_button_link.allow_tags = True
    confirm_button_link.short_description = u'注册审核'


class BankContactor(models.Model):
    user = models.OneToOneField(User, blank=False, null=False, verbose_name=u'登陆账号')
    bank = models.OneToOneField(Bank, blank=False, null=False, verbose_name=u'所属银行', related_name='contactor')
    username = models.CharField(unique=True, max_length=30, blank=False, null=False, verbose_name=u'用户名', help_text=u'长度小于30，只限字母、数字及符号@.+-_')
    # groupname = models.CharField(max_length=20, blank=True, null=True, choices=MEMBER_USER_TYPE, verbose_name=u'角色名称', help_text=u'角色名称')
    name = models.CharField(max_length=50, blank=False, null=False, verbose_name=u'姓名')
    identity_card = models.CharField(max_length=20, blank=False, null=False, verbose_name=u'身份证')
    mobile_number = models.BigIntegerField(max_length=15, blank=False, null=False, verbose_name=u'手机号')
    telephone = models.BigIntegerField(max_length=11, blank=True, null=True, verbose_name=u'固定电话')
    email = models.EmailField(max_length=50, blank=False, null=False, verbose_name=u'电子邮箱')
    # fax_number = models.BigIntegerField(max_length=20, blank=True, null=True, verbose_name=u'传真号')
    position = models.CharField(max_length=20, blank=True, null=True, verbose_name=u'职位')
    pwd_question = models.CharField(max_length=100, blank=False, null=False, verbose_name=u'密码提示问题')
    pwd_answer = models.CharField(max_length=50, blank=False, null=False, verbose_name=u'密码提示问题答案')
    last_login = models.DateTimeField(blank=True, null=True, editable=False, verbose_name=u'上次登录时间')
    create_date = models.DateTimeField(auto_now_add=True, editable=True, verbose_name=u'创建时间')
    modify_date = models.DateTimeField(auto_now_add=True, auto_now=True, editable=True, verbose_name=u'最后修改时间')

    class Meta:
        verbose_name = u'银行会员主联络人'
        verbose_name_plural = u'银行会员主联络人'
        unique_together = (('user', 'bank'),)

    def __unicode__(self):
        return u'[%s主联络人]%s' % (self.bank.name, self.name)
        # return self.name

    @property
    def groupname(self):
        if self.user.groups.count() > 0:
            return self.user.groups.all()[0].name
        else:
            return None

    @property
    def is_contactor(self):
        return True

    @property
    def member_type(self):
        return 'bank'

    @property
    def contactor_id(self):
        return self.id

    @property
    def member_id(self):
        return self.bank_id


class BankOperator(models.Model):
    user = models.OneToOneField(User, blank=True, null=True, verbose_name=u'登陆账号')
    bank = models.ForeignKey(Bank, blank=False, null=False, verbose_name=u'所属银行', related_name='operator_set')
    username = models.CharField(unique=True, max_length=30, blank=False, null=False, verbose_name=u'用户名', help_text=u'长度小于30，只限字母、数字及符号@.+-_')
    # groupname = models.CharField(max_length=20, blank=True, null=True, choices=MEMBER_USER_TYPE, verbose_name=u'角色名称', help_text=u'角色名称')
    name = models.CharField(max_length=50, blank=False, null=False, verbose_name=u'姓名')
    identity_card = models.CharField(max_length=20, blank=False, null=False, verbose_name=u'身份证')
    mobile_number = models.BigIntegerField(max_length=11, blank=False, null=False, verbose_name=u'手机号')
    telephone = models.BigIntegerField(max_length=11, blank=True, null=True, verbose_name=u'固定电话')
    email = models.EmailField(max_length=50, blank=False, null=False, verbose_name=u'电子邮箱')
    # fax_number = models.BigIntegerField(max_length=11, blank=True, null=True, verbose_name=u'传真号')
    position = models.CharField(max_length=20, blank=True, null=True, verbose_name=u'职位')
    pwd_question = models.CharField(max_length=100, blank=True, null=True, verbose_name=u'密码提示问题')
    pwd_answer = models.CharField(max_length=50, blank=True, null=True, verbose_name=u'密码提示问题答案')
    last_login = models.DateTimeField(blank=True, null=True, editable=False, verbose_name=u'上次登录时间')
    create_date = models.DateTimeField(auto_now_add=True, editable=True, verbose_name=u'创建时间')
    modify_date = models.DateTimeField(auto_now_add=True, auto_now=True, editable=True, verbose_name=u'最后修改时间')

    class Meta:
        verbose_name = u'银行会员执行人'
        verbose_name_plural = u'银行会员执行人'
        unique_together = (('user', 'bank'),)

    def __unicode__(self):
        return u'[%s执行人]%s' % (self.bank.name, self.name)

    @property
    def groupname(self):
        if self.user.groups.count() > 0:
            return self.user.groups.all()[0].name
        else:
            return None

    @property
    def is_contactor(self):
        return False

    @property
    def member_type(self):
        return 'bank'

    @property
    def contactor_id(self):
        return self.bank.contactor.id

    @property
    def member_id(self):
        return self.bank_id

# ====================================================== ATTACHMENT ==============================================

STRATEGIC_AGREEMENT = U'战略合作协议'
EXECUTION_AGREEMENT = U'执行合作协议'

BANK_ATTACHMENT_TYPE = (
    (STRATEGIC_AGREEMENT, STRATEGIC_AGREEMENT),
    (EXECUTION_AGREEMENT, EXECUTION_AGREEMENT),

)
import datetime


def get_bank_attachment_path(instance, filename):
    time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    base, ext = os.path.splitext(filename)
    if instance.type == STRATEGIC_AGREEMENT:
        filename = '%s_%s%s' % ('STRATEGIC_AGREEMENT', time, ext)
    else:
        filename = '%s_%s%s' % ('EXECUTION_AGREEMENT', time, ext)
    path = os.path.join('./bank/', str(instance.bank_id), filename)
    return path


def get_bank_attachment_thumbnail_path(instance, filename=None):
    time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    base, ext = os.path.splitext(os.path.basename(instance.file.path))
    if instance.type == STRATEGIC_AGREEMENT:
        filename = '%s_%s%s' % ('STRATEGIC_AGREEMENT', time, ext)
    else:
        filename = '%s_%s%s' % ('EXECUTION_AGREEMENT', time, ext)
    path = os.path.join('./bank/', str(instance.bank_id), 'thumbnail')
    return path


class BankAttachment(models.Model):
    '''
    银行会员信息附件
    '''
    name = models.CharField(unique=True, max_length=50, blank=False, null=False, verbose_name=u'文件名称')
    bank = models.ForeignKey(Bank, blank=False, null=False, verbose_name=u'所属银行')
    type = models.CharField(max_length=50, choices=BANK_ATTACHMENT_TYPE, blank=False, null=False, verbose_name=u'附件内容')
    file = models.FileField(upload_to=get_bank_attachment_path, blank=False, null=False, verbose_name=u'文件')
    thumbnail = models.FileField(upload_to=get_bank_attachment_thumbnail_path, blank=True, null=True, verbose_name=u'缩略文件', help_text=u'仅图片类型文件自动生成')
    extension = models.CharField(max_length=10, blank=False, null=False, verbose_name=u'扩展名')
    size = models.DecimalField(max_digits=10, decimal_places=2, blank=False, null=False, verbose_name=u'文件大小', help_text=u'单位KB')
    width = models.PositiveSmallIntegerField(max_length=10, blank=True, null=True, verbose_name=u'宽度', help_text=u'图片宽度，仅当文件类型为图片时')
    height = models.PositiveSmallIntegerField(max_length=10, blank=True, null=True, verbose_name=u'高度', help_text=u'图片高度，仅当文件类型为图片时')
    need_login = models.BooleanField(default=True, verbose_name=u'需要登陆', help_text=u'需要登陆才能下载')
    creator = models.ForeignKey(User, blank=False, null=False, verbose_name=u'操作用户')
    create_time = models.DateTimeField(auto_now_add=True, editable=True, verbose_name=u'创建时间')

    class Meta:
        verbose_name = u'银行会员附件'
        verbose_name_plural = u'银行会员附件'

    def __unicode__(self):
        return self.name

    def get_link(self):
        return u'<a href="/bank/%s/attachment/%s">链接地址</a>' % (self.bank_id, urlquote(self.name))

    get_link.allow_tags = True
    get_link.short_description = u'链接地址'

    def get_thumbnail_link(self):
        if self.thumbnail:
            return u'<a href="/bank/%s/attachment/thumbnail/%s">缩略图地址</a>' % (self.bank_id, urlquote(self.name))
        else:
            return ''

    get_thumbnail_link.allow_tags = True
    get_thumbnail_link.short_description = u'缩略图地址'

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        # automatically fill size name ext
        self.size = float(self.file.size) / 1000
        base, ext = os.path.splitext(os.path.basename(self.file.path))
        self.extension = ext.replace('.', '').lower()
        super(BankAttachment, self).save(force_insert, force_update, using, update_fields)
        self.name = os.path.basename(self.file.path)

        # if image file , fill width and height, generate thumbnail automatically
        if self.extension == 'jpg' or self.extension == 'png' or self.extension == 'gif' or self.extension == 'jpeg':
            img = Image.open(self.file)
            self.width, self.height = img.size
            thumb_path = os.path.join(MEDIA_ROOT, get_bank_attachment_thumbnail_path(self, self.file.path))
            filename = make_thumb(self.file.path, thumb_path, 100)
            self.thumbnail = 'bank/%s/thumbnail/%s' % (self.bank_id, filename)

        super(BankAttachment, self).save(force_insert, force_update, using, update_fields)


LICENCE = U'营业执照'
ORGANIZATION_CODE = U'机构代码'
TAX_REGISTRATION = U'税务登记证'

ENTERPRISE_ATTACHMENT_TYPE = (
    (LICENCE, LICENCE),
    (ORGANIZATION_CODE, ORGANIZATION_CODE),
    (TAX_REGISTRATION, TAX_REGISTRATION),
)


def get_enterprise_attachment_path(instance, filename):
    time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    base, ext = os.path.splitext(filename)
    if instance.type == LICENCE:
        filename = '%s_%s%s' % ('LICENCE', time, ext)
    elif instance.type == ORGANIZATION_CODE:
        filename = '%s_%s%s' % ('ORGANIZATION_CODE', time, ext)
    elif instance.type == TAX_REGISTRATION:
        filename = '%s_%s%s' % ('TAX_REGISTRATION', time, ext)
    path = os.path.join('./enterprise/', str(instance.enterprise_id), filename)
    return path


def get_enterprise_attachment_thumbnail_path(instance, filename=None):
    time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    base, ext = os.path.splitext(os.path.basename(instance.file.path))
    if instance.type == STRATEGIC_AGREEMENT:
        filename = '%s_%s%s' % ('STRATEGIC_AGREEMENT', time, ext)
    else:
        filename = '%s_%s%s' % ('EXECUTION_AGREEMENT', time, ext)
    path = os.path.join('./enterprise/', str(instance.enterprise_id), 'thumbnail')
    return path


class EnterpriseAttachment(models.Model):
    '''
    银行会员信息附件
    '''
    name = models.CharField(unique=True, max_length=50, blank=False, null=False, verbose_name=u'文件名称')
    enterprise = models.ForeignKey(Enterprise, blank=False, null=False, verbose_name=u'所属企业')
    type = models.CharField(max_length=50, choices=ENTERPRISE_ATTACHMENT_TYPE, blank=False, null=False, verbose_name=u'附件内容')
    file = models.FileField(upload_to=get_enterprise_attachment_path, blank=False, null=False, verbose_name=u'文件')
    thumbnail = models.FileField(upload_to=get_enterprise_attachment_thumbnail_path, blank=True, null=True, verbose_name=u'缩略文件', help_text=u'仅图片类型文件自动生成')
    extension = models.CharField(max_length=10, blank=False, null=False, verbose_name=u'扩展名')
    size = models.DecimalField(max_digits=10, decimal_places=2, blank=False, null=False, verbose_name=u'文件大小', help_text=u'单位KB')
    width = models.PositiveSmallIntegerField(max_length=10, blank=True, null=True, verbose_name=u'宽度', help_text=u'图片宽度，仅当文件类型为图片时')
    height = models.PositiveSmallIntegerField(max_length=10, blank=True, null=True, verbose_name=u'高度', help_text=u'图片高度，仅当文件类型为图片时')
    need_login = models.BooleanField(default=True, verbose_name=u'需要登陆', help_text=u'需要登陆才能下载')
    creator = models.ForeignKey(User, blank=True, null=True, verbose_name=u'操作用户')
    create_time = models.DateTimeField(auto_now_add=True, editable=True, verbose_name=u'创建时间')

    class Meta:
        verbose_name = u'企业会员附件'
        verbose_name_plural = u'企业会员附件'

    def __unicode__(self):
        return self.name

    def get_link(self):
        return u'<a href="/enterprise/%s/attachment/%s">链接地址</a>' % (self.enterprise_id, urlquote(self.name))

    get_link.allow_tags = True
    get_link.short_description = u'链接地址'

    def get_thumbnail_link(self):
        if self.thumbnail:
            return u'<a href="/enterprise/%s/attachment/thumbnail/%s">缩略图地址</a>' % (self.enterprise_id, urlquote(self.name))
        else:
            return ''

    get_thumbnail_link.allow_tags = True
    get_thumbnail_link.short_description = u'缩略图地址'

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        # automatically fill size name ext
        self.size = float(self.file.size) / 1000
        base, ext = os.path.splitext(os.path.basename(self.file.path))
        self.extension = ext.replace('.', '').lower()
        super(EnterpriseAttachment, self).save(force_insert, force_update, using, update_fields)
        self.name = os.path.basename(self.file.path)

        # if image file , fill width and height, generate thumbnail automatically
        if self.extension == 'jpg' or self.extension == 'png' or self.extension == 'gif' or self.extension == 'jpeg':
            img = Image.open(self.file)
            self.width, self.height = img.size
            thumb_path = os.path.join(MEDIA_ROOT, get_enterprise_attachment_thumbnail_path(self, self.file.path))
            filename = make_thumb(self.file.path, thumb_path, 100)
            self.thumbnail = 'enterprise/%s/thumbnail/%s' % (self.enterprise_id, filename)

        super(EnterpriseAttachment, self).save(force_insert, force_update, using, update_fields)





