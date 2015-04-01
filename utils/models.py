#coding=utf-8


from utils.user import *
from TTMS.settings import MEDIA_URL, MEDIA_ROOT, BASE_URL
from django.utils.http import urlquote
from PIL import Image
import os
from utils.func import make_thumb
from django.db import transaction
from django.core import validators
from django.utils.translation import ugettext_lazy as _
from django.utils.crypto import get_random_string

ENTERPRISE_TRUST_AGREEMENT = u'诚信合作协议'
DELEGATE_AGREEMENT = u'委托代理协议'
DELEGATE_STATEMENT = u'委托代理声明'
BANK_STRATEGIC_COOPERATION_AGREEMENT = u'战略合作协议'
BANK_EXECUTION_AGREEMENT = u'执行协议'
TICKET_DELIVERY_RECEIPT = u'承兑汇票交接单据'
TRANSACTION_TICKET = u'承兑汇票'
COMMITMENT1 = U'承诺书1'  # for 银行
COMMITMENT2 = U'承诺书2'  # for 企业

ATTACHMENT_TYPE = (
    (ENTERPRISE_TRUST_AGREEMENT, ENTERPRISE_TRUST_AGREEMENT),
    (DELEGATE_AGREEMENT, DELEGATE_AGREEMENT),
    (DELEGATE_STATEMENT, DELEGATE_STATEMENT),
    (BANK_STRATEGIC_COOPERATION_AGREEMENT, BANK_STRATEGIC_COOPERATION_AGREEMENT),
    (BANK_EXECUTION_AGREEMENT, BANK_EXECUTION_AGREEMENT),
    (TICKET_DELIVERY_RECEIPT, TICKET_DELIVERY_RECEIPT),
    (TRANSACTION_TICKET, TRANSACTION_TICKET),
    (COMMITMENT1, COMMITMENT1),
    (COMMITMENT2, COMMITMENT2),
)


def get_template_attachment_path(instance, filename):
    time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    base, ext = os.path.splitext(filename)
    filename = '%s%s' % (time, ext)

    path = os.path.join('./template_document/', filename)
    return path


class TemplateAttachment(models.Model):
    '''
    附件
    '''
    type = models.CharField(max_length=50, choices=ATTACHMENT_TYPE, blank=False, null=False, verbose_name=u'附件内容')
    file = models.FileField(upload_to=get_template_attachment_path, blank=False, null=False, verbose_name=u'文件')
    thumbnail = models.FileField(upload_to='./template_document/thumbnail', blank=True, null=True, verbose_name=u'缩略文件', help_text=u'仅图片类型文件自动生成')
    name = models.CharField(unique=True, max_length=50, blank=False, null=False, verbose_name=u'文件名称')
    extension = models.CharField(max_length=10, blank=False, null=False, verbose_name=u'扩展名')
    size = models.DecimalField(max_digits=10, decimal_places=2, blank=False, null=False, verbose_name=u'文件大小', help_text=u'单位KB')
    width = models.PositiveSmallIntegerField(max_length=10, blank=True, null=True, verbose_name=u'宽度', help_text=u'图片宽度，仅当文件类型为图片时')
    height = models.PositiveSmallIntegerField(max_length=10, blank=True, null=True, verbose_name=u'高度', help_text=u'图片高度，仅当文件类型为图片时')
    need_login = models.BooleanField(default=True, verbose_name=u'需要登陆', help_text=u'需要登陆才能下载')
    creator = models.ForeignKey(User, blank=True, null=True, verbose_name=u'操作用户')
    create_time = models.DateTimeField(auto_now_add=True, editable=True, verbose_name=u'创建时间')

    class Meta:
        verbose_name = u'文档模板'
        verbose_name_plural = u'文档模板'

    def __unicode__(self):
        return self.name

    def get_link(self):
        return u'<a href="/template/%s">链接地址</a>' % urlquote(self.name)

    get_link.allow_tags = True
    get_link.short_description = u'链接地址'

    def get_url(self):
        return '%s/template/%s' % (BASE_URL, urlquote(self.name))

    def get_thumbnail_link(self):
        if self.thumbnail:
            return u'<a href="/template/thumbnail/%s">缩略图地址</a>' % urlquote(self.name)
        else:
            return None

    get_thumbnail_link.allow_tags = True
    get_thumbnail_link.short_description = u'缩略图地址'

    def get_thumbnail_url(self):
        if self.thumbnail:
            return '%s/template/thumbnail/%s' % (BASE_URL, urlquote(self.name))
        else:
            return None

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        # automatically fill size name ext
        self.size = float(self.file.size) / 1000
        #self.name = self.file.name
        base, ext = os.path.splitext(os.path.basename(self.file.path))
        self.extension = ext.replace('.', '').lower()
        super(TemplateAttachment, self).save(force_insert, force_update, using, update_fields)
        self.name = os.path.basename(self.file.path)

        # if image file , fill width and height, generate thumbnail automatically
        if self.extension == 'jpg' or self.extension == 'png' or self.extension == 'gif' or self.extension == 'jpeg':
            img = Image.open(self.file)
            self.width, self.height = img.size
            filename = make_thumb(self.file.path, os.path.join(MEDIA_ROOT, 'template_document', 'thumbnail'), 100)
            self.thumbnail = 'template_document/thumbnail/' + filename

        super(TemplateAttachment, self).save(force_insert, force_update, using, update_fields)


MEMBER_REGISTRATION = 'MEMBER_REGISTRATION'
BANK_CONTACTOR_MOBILE = 'BANK_CONTACTOR_MOBILE'
BANK_OPERATOR_MOBILE = 'BANK_OPERATOR_MOBILE'
ENTERPRISE_CONTACTOR_MOBILE = 'ENTERPRISE_CONTACTOR_MOBILE'
ENTERPRISE_OPERATOR_MOBILE = 'ENTERPRISE_OPERATOR_MOBILE'

VERIFYCODE_TYPE = (
    (MEMBER_REGISTRATION, '会员注册'),
    (BANK_CONTACTOR_MOBILE, '银行主联络人手机验证'),
    (BANK_OPERATOR_MOBILE, '银行执行人手机验证'),
    (ENTERPRISE_CONTACTOR_MOBILE, '企业主联络人手机验证'),
    (ENTERPRISE_OPERATOR_MOBILE, '企业执行人手机验证'),
)


class SMSVerifyCode(models.Model):
    type = models.CharField(max_length=50, choices=VERIFYCODE_TYPE, blank=False, null=False, verbose_name=u'验证码类型')
    key = models.CharField(unique=True, max_length=50, blank=False, null=False, verbose_name=u'验证码标识')
    mobile = models.CharField(max_length=13, blank=False, null=False, verbose_name=u'手机号码',
                              validators=[validators.RegexValidator(r'^[\d+]+$', _(u'手机号码不正确'), 'mobile_invalid'), ])
    code = models.PositiveSmallIntegerField(max_length=8, blank=True, null=True, verbose_name=u'验证码',
                                            validators=[validators.RegexValidator(r'^[\d+]+$', _(u'验证码格式不正确'), 'code_invalid'), ])
    create_time = models.DateTimeField(auto_now_add=True, editable=True, verbose_name=u'创建时间')


def generate_sms_verify_code(type, key, mobile):
    code = get_random_string(6, '1234567890')
    code_record = SMSVerifyCode(type=type, key=key, mobile=mobile, code=code)
    code_record.save()


def generate_email_verify_code(username, mobile):
    pass