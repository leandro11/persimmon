#coding=utf-8

from django.db import models
from django.contrib.auth.models import User, UserManager
from django.core.exceptions import ObjectDoesNotExist
from django.utils.safestring import mark_safe

from member.models import *
from management.models import *
from utils.constants import *
from utils.constants import (
    TransactionClaimStatus, CLAIM_STATUS, InvoiceStatus, INVOICE_STATUS,
    INVOICE_STATUS2, TicketStatus, TICKET_STATUS, TICKET_STATUS2,
    TransactionStatus, TRANSACTION_STATUS, TransactionCategory,
    TRANSACTION_TYPE, OperationStatus, OPERATION_STATUS, OperationType,
    OPERATION_TYPE, OperatorType, OPERATOR_TYPE)


class TransactionType(models.Model):
    '''
    贴现服务类型
    '''
    name = models.CharField(
        unique=True, max_length=50, choices=TRANSACTION_TYPE,
        default=TransactionCategory.get_description(TransactionCategory.TRANSACTION_TYPE1),
        verbose_name=u'贴现服务类型'
    )
    fee = models.DecimalField(
        max_digits=10, decimal_places=2, blank=False,
        null=False, verbose_name=u'服务费率'
    )

    class Meta:
        verbose_name = u'贴现服务类型'
        verbose_name_plural = u'贴现服务类型'

    def __unicode__(self):
        return self.name


class TransactionMetaOperation(models.Model):
    '''
    贴现流程模板
    '''
    transaction_type = models.ForeignKey(TransactionType, blank=False, null=False, verbose_name=u'贴现服务类型')
    sequence = models.SmallIntegerField(max_length=5, verbose_name=u'顺序')
    operation_type = models.CharField(max_length=30, blank=False, null=False, choices=OPERATION_TYPE, default=OperationType.OPERATION_CONFIRM, verbose_name=u'操作类型')
    operator_member = models.CharField(max_length=30, blank=False, null=False, choices=OPERATOR_TYPE, verbose_name=u'执行方')
    description = models.TextField(max_length=500, blank=False, null=False, verbose_name=u'操作描述')
    file_name = models.CharField(max_length=30, blank=True, null=True, verbose_name=u'附件名称')
    need_upload = models.BooleanField(default=False, verbose_name=u'附件上传')
    need_ems = models.BooleanField(default=False, verbose_name=u'有EMS')
    need_confirm = models.BooleanField(default=False, verbose_name=u'需客服确认')

    class Meta:
        verbose_name = u'贴现流程操作模板'
        verbose_name_plural = u'贴现流程操作模板'
        ordering = ('sequence',)
        unique_together = (('transaction_type', 'sequence'),)

    def __unicode__(self):
        return ''


class TransactionClaim(models.Model):
    '''
    贴现申请记录，由收款企业填写
    '''
    ticket_number = models.CharField(unique=True, max_length=50, blank=True, null=True, verbose_name=u'汇票单号')
    receivable_enterprise = models.ForeignKey(Enterprise, blank=False, null=False, verbose_name=u'收款企业')
    payee_rate = models.CharField(max_length=50, blank=True, null=True, verbose_name=u'收款方银行评级')
    payee_rate_file = models.ImageField(upload_to='.', blank=True, null=True, verbose_name=u'银行评级扫描件', help_text=mark_safe('<a target="_blank" href="">银行评级说明</a>'))
    payee_bad_credit = models.TextField(max_length=500, blank=True, null=True, verbose_name=u'收款方不良信征', help_text='')

    payee_net_income = models.DecimalField(max_digits=11, decimal_places=2, blank=False, null=False, verbose_name=u'营收入额', help_text='单位：万元 *必填')
    payee_asset_size = models.DecimalField(max_digits=11, decimal_places=2, blank=False, null=False, verbose_name=u'资产规模', help_text='单位：万元 *必填')
    payee_debt_promise = models.BooleanField(blank=False, null=False, default=False, verbose_name=u'企业负债率承诺', help_text='承诺连同贴现贷款，企业的资产负债率不高于70% *必填')

    pay_enterprise = models.CharField(max_length=50, blank=False, null=False, verbose_name=u'付款企业', help_text='*必填')
    ticket_bank = models.CharField(max_length=50, blank=False, null=False, verbose_name=u'贴现银行', help_text='*必填')
    accept_bank = models.CharField(max_length=50, blank=False, null=False, verbose_name=u'承兑银行', help_text='*必填')
    amount = models.DecimalField(max_digits=11, decimal_places=2, blank=False, null=False, verbose_name=u'金额', help_text='*必填')

    status = models.CharField(
        max_length=20, choices=CLAIM_STATUS,
        default=TransactionClaimStatus.CLAIM_PENDING, verbose_name=u'贴现发起状态'
    )
    create_time = models.DateTimeField(auto_now_add=True, editable=True, verbose_name=u'创建时间')

    class Meta:
        verbose_name = u'贴现申请'
        verbose_name_plural = u'贴现申请记录'
        permissions = (("confirm_transactionclaim", u"审核贴现申请"),)

    def __unicode__(self):
        if self.ticket_number:
            return u'[贴现申请]%s' % self.ticket_number
        else:
            return u'[贴现申请]%s 付款至 %s' % (self.pay_enterprise, self.receivable_enterprise.name)

    def name_link(self):
        if self.ticket_number:
            return u'<a href="/transaction/transactionclaim/%s"><strong>%s</strong></a>' % (self.id, self.ticket_number)
        else:
            return u'%s 付款至 %s' % (self.pay_enterprise, self.receivable_enterprise.name)

    name_link.allow_tags = True
    name_link.short_description = u'汇票单号'

    def confirm_number_link(self):
        name = self.ticket_number if self.ticket_number else u'%s 付款至 %s' % (self.pay_enterprise, self.receivable_enterprise.name)
        return u'<a href="/staff/transaction/transactionclaim/%s/confirm">%s</a>' % (self.id, name)

    confirm_number_link.allow_tags = True
    confirm_number_link.short_description = u'汇票单号'

    def confirm_button_link(self):
        return u'<a class="button" href="/staff/transaction/transactionclaim/%s/confirm">进行审核</a>' % self.id

    confirm_button_link.allow_tags = True
    confirm_button_link.short_description = u'注册审核'


class TransactionOrder(models.Model):
    '''
    贴现服务订单，客服确认贴现发起记录后生成
    '''
    transaction_claim = models.OneToOneField(TransactionClaim, blank=False, null=False, verbose_name=u'贴现申请', related_name='order')
    ticket_number = models.CharField(unique=True, max_length=50, blank=False, null=False, verbose_name=u'汇票单号')
    receivable_enterprise = models.ForeignKey(Enterprise, related_name='receivable_enterprise', blank=False, null=False, verbose_name=u'收款企业')
    pay_enterprise = models.ForeignKey(Enterprise, related_name='pay_enterprise', blank=False, null=False, verbose_name=u'付款企业')
    ticket_bank = models.ForeignKey(Bank, related_name='ticket_bank', blank=False, null=False, verbose_name=u'贴现银行')
    accept_bank = models.ForeignKey(Bank, related_name='accept_bank', blank=False, null=False, verbose_name=u'承兑银行')
    amount = models.DecimalField(max_digits=11, decimal_places=2, blank=False, null=False, verbose_name=u'贴现金额')
    type = models.ForeignKey(TransactionType, blank=False, null=False, verbose_name=u'贴现服务类型')
    fee = models.DecimalField(max_digits=10, decimal_places=2, blank=False, null=False, verbose_name=u'服务费  ')
    invoice_status = models.CharField(
        max_length=30, choices=INVOICE_STATUS2,
        default=InvoiceStatus.INVOICE_UNLODGED, verbose_name=u'发票状态'
    )
    ticket_status = models.CharField(
        max_length=30, choices=TICKET_STATUS2,
        default=TicketStatus.TICKET_UNRECEIVED, verbose_name=u'汇票状态'
    )
    status = models.CharField(max_length=20, choices=TRANSACTION_STATUS, default=TransactionStatus.TRANSACTION_PROCESSING, verbose_name=u'贴现订单状态')
    # ticket = models.OneToOneField(TransactionTicket, blank=True, null=True, verbose_name=u'汇票')
    # invoice = models.OneToOneField(Invoice, blank=True, null=True, verbose_name=u'发票')
    create_time = models.DateTimeField(auto_now_add=True, editable=True, verbose_name=u'创建时间')
    finish_time = models.DateTimeField(blank=True, null=True, editable=True, verbose_name=u'完成时间', default=None)
    modify_time = models.DateTimeField(auto_now_add=True, auto_now=True, editable=True, verbose_name=u'最后修改时间')

    class Meta:
        verbose_name = u'贴现服务订单'
        verbose_name_plural = u'贴现服务订单'

    def __unicode__(self):
        return u'[贴现订单]%s' % self.ticket_number

    def name_link(self):
        return u'<a href="/transaction/transactionorder/%s"><strong>%s</strong></a>' % (self.id, self.ticket_number)

    name_link.allow_tags = True
    name_link.short_description = u'汇票单号'


class TicketFormerHolder(models.Model):
    '''
    历史持票人
    '''
    name = models.CharField(max_length=50, blank=False, null=False, verbose_name=u'持票人名称')
    claim = models.ForeignKey(TransactionClaim, blank=False, null=False, verbose_name=u'贴现发起记录')
    transaction = models.ForeignKey(TransactionOrder, blank=True, null=True, verbose_name=u'贴现服务订单')

    class Meta:
        verbose_name = u'历史持票人'
        verbose_name_plural = u'历史持票人'

    def __unicode__(self):
        return u'[历史持票人]%s' % self.name


def get_operation_attachment_path(instance, filename):
    time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    base, ext = os.path.splitext(filename)
    # if instance.type == LICENCE:
    #     filename = '%s_%s%s' % ('LICENCE', time, ext)
    # elif instance.type == ORGANIZATION_CODE:
    #     filename = '%s_%s%s' % ('ORGANIZATION_CODE', time, ext)
    # elif instance.type == TAX_REGISTRATION:
    #     filename = '%s_%s%s' % ('TAX_REGISTRATION', time, ext)
    filename = '%s_%s%s' % (instance.id, time, ext)
    path = os.path.join('./operation/', str(instance.transaction_id), filename)
    return path


def get_operation_attachment_thumbnail_path(instance, filename):
    time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    base, ext = os.path.splitext(filename)
    filename = '%s_%s%s' % (instance.id, time, ext)
    path = os.path.join('./operation/', str(instance.transaction_id), 'thumbnail')
    return path


class TransactionOperation(models.Model):
    '''
    贴现流程操作
    '''
    transaction = models.ForeignKey(TransactionOrder, blank=False, null=False, verbose_name=u'贴现服务订单')
    sequence = models.SmallIntegerField(max_length=5, verbose_name=u'顺序')
    operator_member = models.CharField(max_length=30, choices=OPERATOR_TYPE, verbose_name=u'执行方')
    # operator_member_type = models.CharField(max_length=30, choices=MEMBER_TYPE, default=MEMBER_PLATFORM, blank=False, null=False, verbose_name=u'执行方类型')
    # operator_member_id = models.BigIntegerField(max_length=30, blank=False, null=False, verbose_name=u'执行方编号')
    operation_type = models.CharField(max_length=30, choices=OPERATION_TYPE, default=OperationType.OPERATION_CONFIRM, verbose_name=u'操作类型')
    description = models.TextField(max_length=500, blank=False, null=False, verbose_name=u'操作描述')
    operator_user = models.ForeignKey(User, blank=True, null=True, verbose_name=u'执行人')
    need_upload = models.BooleanField(default=False, verbose_name=u'附件上传')
    file_name = models.CharField(max_length=30, blank=True, null=True, verbose_name=u'附件名称')
    upload_file = models.FileField(upload_to=get_operation_attachment_path, blank=True, null=True, verbose_name=u'附件文件')
    upload_file_name = models.CharField(max_length=50, blank=True, null=True, verbose_name=u'附件名称')
    upload_file_thumbnail = models.FileField(upload_to=get_operation_attachment_thumbnail_path, blank=True, null=True, verbose_name=u'附件缩略图', help_text=u'仅图片类型文件自动生成')
    need_ems = models.BooleanField(default=False, verbose_name=u'需要EMS')
    ems_number = models.CharField(max_length=30, blank=True, null=True, verbose_name=u'EMS单号')
    need_confirm = models.BooleanField(default=False, verbose_name=u'需客服确认')
    confirm_service = models.ForeignKey(Staff, blank=True, null=True, verbose_name=u'审核客服')
    status = models.CharField(max_length=30, choices=OPERATION_STATUS, default=OperationStatus.OPERATION_UNACTIVATED, verbose_name=u'操作状态')
    remark = models.CharField(max_length=200, blank=True, null=True, verbose_name=u'备注')
    available_time = models.DateTimeField(blank=True, null=True, editable=True, verbose_name=u'激活时间', default=None)
    finish_time = models.DateTimeField(blank=True, null=True, editable=True, verbose_name=u'完成时间', default=None)

    class Meta:
        verbose_name = u'贴现操作'
        verbose_name_plural = u'贴现操作'
        ordering = ('sequence',)

    def __unicode__(self):
        return u'[贴现操作]%s' % self.description

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.upload_file:
            super(TransactionOperation, self).save(force_insert, force_update, using, update_fields)
            # automatically generate thumbnail
            self.upload_file_name = os.path.basename(self.upload_file.path)
            ext = os.path.splitext(self.upload_file_name)[1].replace('.', '').lower()
            if ext == 'jpg' or ext == 'png' or ext == 'gif' or ext == 'jpeg':
                img = Image.open(self.upload_file)
                thumb_path = os.path.join(MEDIA_ROOT, get_operation_attachment_thumbnail_path(self, self.upload_file.path))
                filename = make_thumb(self.upload_file.path, thumb_path, 100)
                self.upload_file_thumbnail = os.path.join('operation/', str(self.transaction_id), 'thumbnail', filename)

        super(TransactionOperation, self).save(force_insert, force_update, using, update_fields)

        # through='Membership', through_fields=('group', 'person')