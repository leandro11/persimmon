#coding=utf-8

import sys
import datetime

from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.shortcuts import get_object_or_404, render_to_response, render, redirect
from django.http import HttpResponse
from django.conf.urls import patterns
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from django.db import transaction
from django.contrib.admin.exceptions import DisallowedModelAdminToField
from django.core.exceptions import (PermissionDenied, ValidationError, FieldError, ImproperlyConfigured)
from django.http import Http404, HttpResponseRedirect
from django.contrib.admin.utils import (quote, unquote, flatten_fieldsets, get_deleted_objects, model_format_dict, NestedObjects, lookup_needs_distinct)
from django.core.urlresolvers import reverse
from django.utils.encoding import force_text, python_2_unicode_compatible
from django.utils.html import escape, escapejs
from django.forms.formsets import all_valid, DELETION_FIELD_NAME
from django.contrib.admin import widgets, helpers
from django.utils.translation import ugettext as _
from django.db import transaction
from django.contrib.auth import get_permission_codename
from django.template.response import SimpleTemplateResponse, TemplateResponse
from django.contrib import messages
from django.contrib.messages.storage.fallback import FallbackStorage
from django.http import Http404, HttpResponseNotFound

from member.sites import site as member_site
from ticket.form import *
from transaction.form import *
from utils.constants import StaffType
from management.sites import site as management_site
from transaction.models import *
from utils.constants import (
    MemberUserType, MEMBER_USER_TYPE, TransactionClaimStatus,
    CLAIM_STATUS, TransactionStatus, InvoiceStatus, TicketStatus,
    MemberType, OperationStatus, OPERATION_STATUS, OperationType,
    OPERATION_TYPE, OperatorType, OPERATOR_TYPE)
from utils.user import group_check, get_group, get_user_profile

reload(sys)
sys.setdefaultencoding('utf-8')

csrf_protect_m = method_decorator(csrf_protect)
IS_POPUP_VAR = '_popup'
TO_FIELD_VAR = '_to_field'


class TransactionTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'fee']
    readonly_fields = []
    search_fields = ['name', ]
    list_filter = ['name', 'fee']

    @transaction.atomic
    def add_view(self, request, form_url='', extra_context=None):
        self.exclude = []
        self.readonly_fields = []
        self.inlines = [TransactionMetaOperationAddInline]
        # if request.user.is_superuser:
        #     return super(TransactionTypeAdmin, self).add_view(request, form_url, extra_context)

        # user_profile = get_user_profile(request.user)
        # # 只有总经理有权限编辑贴现类型
        # if user_profile.groupname != TOP_MANAGER:
        #     raise PermissionDenied

        to_field = request.POST.get(TO_FIELD_VAR, request.GET.get(TO_FIELD_VAR))
        if to_field and not self.to_field_allowed(request, to_field):
            raise DisallowedModelAdminToField("The field %s cannot be referenced." % to_field)

        model = self.model
        opts = model._meta
        add = True
        object_id = None
        if not self.has_add_permission(request):
            raise PermissionDenied
        obj = None

        ModelForm = self.get_form(request, obj)
        if request.method == 'POST':
            form = ModelForm(request.POST, request.FILES, instance=obj)
            if form.is_valid():
                form_validated = True
                new_object = self.save_form(request, form, change=not add)
            else:
                form_validated = False
                new_object = form.instance
            formsets, inline_instances = self._create_formsets(request, new_object)
            if all_valid(formsets) and form_validated:
                self.save_model(request, new_object, form, not add)
                form.save_m2m()
                for formset in formsets:
                    i = 1
                    for inline_form in formset.forms:
                        if isinstance(inline_form, TransactionMetaOperationForm):
                            inline_form.instance.sequence = i * 10
                            # inline_form.save()
                            i += 1
                    formset.save()

                self.log_addition(request, new_object)
                return self.response_add(request, new_object)

        else:
            initial = self.get_changeform_initial_data(request)
            form = ModelForm(initial=initial)
            formsets, inline_instances = self._create_formsets(request, self.model())

        adminForm = helpers.AdminForm(
            form,
            list(self.get_fieldsets(request, obj)),
            self.get_prepopulated_fields(request, obj),
            self.get_readonly_fields(request, obj),
            model_admin=self)
        media = self.media + adminForm.media

        inline_formsets = self.get_inline_formsets(request, formsets, inline_instances, obj)
        for inline_formset in inline_formsets:
            media = media + inline_formset.media

        context = dict(self.admin_site.each_context(),
                       title=(_('Add %s') if add else _('Change %s')) % force_text(opts.verbose_name),
                       adminform=adminForm,
                       object_id=object_id,
                       original=obj,
                       is_popup=(IS_POPUP_VAR in request.POST or
                                 IS_POPUP_VAR in request.GET),
                       to_field=to_field,
                       media=media,
                       inline_admin_formsets=inline_formsets,
                       errors=helpers.AdminErrorList(form, formsets),
                       preserved_filters=self.get_preserved_filters(request),
        )

        context.update(extra_context or {})

        return self.render_change_form(request, context, add=add, change=not add, obj=obj, form_url=form_url)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        self.exclude = []
        self.readonly_fields = []
        self.inlines = [TransactionMetaOperationChangeInline]
        return super(TransactionTypeAdmin, self).change_view(request, object_id, form_url, extra_context)

    def get_queryset(self, request):
        qs = super(TransactionTypeAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        user_profile = get_user_profile(request.user)
        group_name = None if user_profile is None else user_profile.groupname

        if isinstance(user_profile, Staff):
            return qs
        else:
            raise PermissionDenied


admin.site.register(TransactionType, TransactionTypeAdmin)
# member_site.register(TransactionType, TransactionTypeAdmin)
management_site.register(TransactionType, TransactionTypeAdmin)


class TransactionClaimAdmin(admin.ModelAdmin):
    search_fields = ['ticket_number']
    list_display = [
        'name_link', 'receivable_enterprise', 'pay_enterprise',
        'ticket_bank', 'accept_bank', 'amount'
    ]
    inlines = []
    exclude = []
    readonly_fields = []
    form = ModelForm

    def get_urls(self):
        urls = super(TransactionClaimAdmin, self).get_urls()
        my_urls = patterns('',
                           (r'^(.+)/confirm/$', self.confirm_view),  # 审核贴现申请，贴现申请记录 -> 贴现服务订单
        )
        return my_urls + urls

    def has_confirm_permission(self, request):
        opts = self.opts
        codename = get_permission_codename('confirm', opts)
        return request.user.has_perm("%s.%s" % (opts.app_label, codename))

    def has_change_permission(self, request, obj=None):
        opts = self.opts
        codename = get_permission_codename('change', opts)
        return request.user.has_perm("%s.%s" % (opts.app_label, codename))

    @transaction.atomic
    def add_view(self, request, form_url='', extra_context=None):
        self.exclude = ['status']
        self.inlines = [TicketFormerHolderAddInline]

        if request.user.is_superuser:
            return super(TransactionClaimAdmin, self).add_view(request, form_url, extra_context)

        user_profile = get_user_profile(request.user)
        group_type = None if user_profile is None else user_profile.grouptype

        # Only enterprise contactor and operator could create transaction apply
        if group_type in (MemberUserType.ENTERPRISE_CONTACTOR, MemberUserType.ENTERPRISE_OPERATOR):
            self.form = TransactionClaimAddForm
            self.change_form_template = 'member/member_change_form.html'
            extra_context = dict(title=u'发起贴现申请', )

            if request.method == 'POST':
                return super(TransactionClaimAdmin, self).add_view(request, form_url, extra_context)
            else:
                # put enterprise_id into get which is passed to TransactionClaimAdmin
                mutable = request.GET._mutable
                request.GET._mutable = True
                request.GET['enterprise_id'] = user_profile.enterprise_id
                request.GET._mutable = mutable
                return super(TransactionClaimAdmin, self).add_view(request, form_url, extra_context)

        # if group_type not in ENTERPRISE_CONTACTOR and ENTERPRISE_OPERATOR
        return render_to_response("member/notify.html", {
            "info": u'<h2>只有企业会员能够发起贴现申请，<a href="/member/main/%s">点击返回会员首页</a></h2>',
            "title": u'非企业会员',
            'user': request.user,
        })

    @transaction.atomic
    def change_view(self, request, object_id, form_url='', extra_context=None):
        self.exclude = []
        self.form = TransactionClaimAddForm

        user_profile = get_user_profile(request.user)
        group_type = None if user_profile is None else user_profile.grouptype

        if request.user.is_superuser:
            return super(TransactionClaimAdmin, self).change_view(request,
                                                                  object_id,
                                                                  form_url,
                                                                  extra_context)

        if group_type in (MemberUserType.ENTERPRISE_CONTACTOR,
                          MemberUserType.ENTERPRISE_OPERATOR):
            return super(TransactionClaimAdmin, self).change_view(request,
                                                                  object_id,
                                                                  form_url,
                                                                  extra_context)

        if group_type in (StaffType.ZONE_SERVICE, StaffType.SERVICE_MANAGER,
                          StaffType.ZONE_MARKET, StaffType.MARKET_MANAGER):
            self.readonly_fields = ['status']
            return super(TransactionClaimAdmin, self).change_view(request,
                                                                  object_id,
                                                                  form_url,
                                                                  extra_context)
        raise PermissionDenied

    @transaction.atomic
    def confirm_view(self, request, object_id, form_url='', extra_context=None):
        self.inlines = [TicketFormerHolderAddInline, TransactionOrderConfirmInline]
        self.exclude = ['status']

        # This application has been confirmed
        claim = TransactionClaim.objects.get(id=long(object_id))
        if claim.status in (TransactionClaimStatus.CLAIM_PASSED,
                            TransactionClaimStatus.CLAIM_ABORT):
            description = TransactionClaimStatus.get_description(claim.status)
            return HttpResponse("贴现申请%s" % description)

        # 把收款企业的ID传递到inline
        mutable = request.GET._mutable
        request.GET._mutable = True
        request.GET['receivable_enterprise_id'] = object_id
        request.GET._mutable = mutable

        self.form = TransactionClaimConfirmForm
        if request.user.is_superuser:
            # todo 更改操作成功后的返回页面
            return super(TransactionClaimAdmin, self).change_view(request,
                                                                  object_id,
                                                                  form_url,
                                                                  extra_context)

        user_profile = get_user_profile(request.user)
        group_type = None if user_profile is None else user_profile.grouptype

        # market manager or zone market manager need to confirm application
        if group_type in (StaffType.MARKET_MANAGER, StaffType.ZONE_MARKET):
            self.change_form_template = 'management/change_form.html'
            result = super(TransactionClaimAdmin, self).change_view(request,
                                                                    object_id,
                                                                    form_url,
                                                                    extra_context)

            # Return HttpResponseRedirect if add successfully, return TemplateResponse if validating failed
            if request.method == 'POST' and isinstance(result, HttpResponseRedirect):
                # reset warning message
                request._messages = FallbackStorage(request)
                self.message_user(request, u'贴现申请已通过审核', messages.SUCCESS)

                # return changelist view
                return super(TransactionClaimAdmin, self).changelist_view(request, extra_context)

            return result

        raise PermissionDenied

    def save_related(self, request, form, formsets, change):
        if request.path.find('/confirm') < 0:
            super(TransactionClaimAdmin, self).save_related(request, form, formsets, change)
        else:
            form.save_m2m()
            order_id = None
            transaction_type_id = None
            receivable_enterprise_id = None
            pay_enterprise_id = None
            ticket_bank_id = None
            accept_bank_id = None
            for formset in formsets:
                if formset.form.Meta.model is TransactionOrder and formset.has_changed():
                    for inline_form in formset.forms:
                        inline_form.instance.ticket_number = form.instance.ticket_number
                        inline_form.instance.amount = form.instance.amount
                        receivable_enterprise_id = form.instance.receivable_enterprise_id
                        pay_enterprise_id = inline_form.instance.pay_enterprise_id
                        ticket_bank_id = inline_form.instance.ticket_bank_id
                        accept_bank_id = inline_form.instance.accept_bank_id
                        transaction_type_id = inline_form.instance.type_id
                        formset.save()
                        order_id = inline_form.instance.id
                elif formset.form.Meta.model is TicketFormerHolder:
                    if transaction_type_id:
                        for inline_form in formset.forms:
                            inline_form.instance.transaction_id = order_id
                            inline_form.save()
                    formset.save()

            # Generate process according to different process templates
            if transaction_type_id:
                is_first = True
                meta_operation_list = TransactionMetaOperation.objects.filter(
                    transaction_type=transaction_type_id).order_by('sequence')
                for meta_operation in meta_operation_list:
                    operation = TransactionOperation(
                        transaction_id=order_id,
                        sequence=meta_operation.sequence,
                        operation_type=meta_operation.operation_type,
                        description=meta_operation.description,
                        need_confirm=meta_operation.need_confirm,
                        need_upload=meta_operation.need_upload,
                        need_ems=meta_operation.need_ems,
                        operator_member=meta_operation.operator_member,
                        file_name=meta_operation.file_name
                    )

                    # active first operation
                    if is_first:
                        operation.status = OperationStatus.OPERATION_ACTIVATED
                        is_first = False
                    operation.save()
            form.instance.status = TransactionClaimStatus.CLAIM_PASSED
            form.instance.save()

    def response_change(self, request, obj):
        if request.path.find('/confirm'):
            # todo 跳转到新生成的贴现服务订单
            return super(TransactionClaimAdmin, self).response_change(request, obj)
        else:
            return super(TransactionClaimAdmin, self).response_change(request, obj)

    def get_queryset(self, request):
        qs = super(TransactionClaimAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        user_profile = get_user_profile(request.user)
        group_type = None if user_profile is None else user_profile.grouptype

        if group_type in (MemberUserType.BANK_CONTACTOR, MemberUserType.BANK_OPERATOR):
            return qs.filter(Q(ticket_bank=user_profile.bank_id) | Q(accept_bank=user_profile.bank_id)).order_by('-id')
        elif group_type in (MemberUserType.ENTERPRISE_OPERATOR, MemberUserType.ENTERPRISE_CONTACTOR):
            return qs.filter(Q(receivable_enterprise=user_profile.enterprise_id) | Q(pay_enterprise=user_profile.enterprise_id)).order_by('-id')
        elif isinstance(user_profile, Staff):
            return qs
        else:
            raise PermissionDenied

    def changelist_view(self, request, extra_context=None):
        self.list_display = ['name_link', 'receivable_enterprise', 'pay_enterprise', 'ticket_bank', 'accept_bank', 'amount', 'status']
        if request.user.is_superuser:
            return super(TransactionClaimAdmin, self).changelist_view(request, extra_context)

        user_profile = get_user_profile(request.user)
        group_name = None if user_profile is None else user_profile.groupname

        # 只允许工作人员用户查看changelist
        if isinstance(user_profile, Staff):
            pass
        else:
            return Http404

        title = u'全部贴现申请'
        if u'status__exact' in request.GET:
            status = request.GET[u'status__exact'].lower()
            if status == TransactionClaimStatus.CLAIM_PENDING.lower():
                self.list_display = ['confirm_number_link', 'receivable_enterprise', 'pay_enterprise', 'ticket_bank', 'accept_bank', 'amount', 'confirm_button_link']
                title = u'待审核的贴现申请'
            elif status == CLAIM_PASSED.lower():
                title = u'审核通过的贴现申请'
            elif status == CLAIM_ABORT.lower():
                title = u'已放弃的贴现申请'

        extra_context = dict(
            title=title,
        )
        return super(TransactionClaimAdmin, self).changelist_view(request, extra_context)


admin.site.register(TransactionClaim, TransactionClaimAdmin)
member_site.register(TransactionClaim, TransactionClaimAdmin)
management_site.register(TransactionClaim, TransactionClaimAdmin)


class TransactionOrderAdmin(admin.ModelAdmin):
    search_fields = ['ticket_number']
    inlines = []
    exclude = ['transaction_claim', ]
    list_display = ['ticket_number', 'amount', 'fee', 'status']
    # list_display = ['ticket_number', 'type', 'receivable_enterprise', 'pay_enterprise', 'ticket_bank', 'accept_bank', 'amount', 'type', 'fee', 'status']
    # 'receivable_enterprise', 'pay_enterprise', 'ticket_bank', 'accept_bank', 'amount', 'type', 'fee', 'status']
    search_fields = ['ticket_number', ]
    list_filter = ['status', ]

    def get_urls(self):
        urls = super(TransactionOrderAdmin, self).get_urls()
        my_urls = patterns('',
                           (r'^(.+)/add_invoice/$', self.add_invoice),  # 开具发票
                           (r'^(.+)/send_invoice/$', self.send_invoice),  # 寄出发票
                           (r'^(.+)/add_ticket/$', self.add_ticket),  # 开具汇票
                           (r'^(.+)/finish/$', self.finish_view),  # 完成贴现
        )
        return my_urls + urls

    @transaction.atomic
    def finish_view(self, request, object_id, form_url='', extra_context=None):
        if not request.method == 'POST':
            return super(TransactionOrderAdmin, self).change_view(request,
                                                                  object_id,
                                                                  form_url,
                                                                  extra_context)

        user_profile = get_user_profile(request.user)
        group_type = None if user_profile is None else user_profile.grouptype

        if not group_type in (StaffType.ZONE_SERVICE, StaffType.SERVICE_MANAGER, StaffType.TOP_MANAGER):
            return render_to_response("management/notify.html", {
                "info": u'仅有客服部总经理、区域客服、总经理有权限执行此操作',
                "title": u'没有权限完成贴现',
                'user': request.user,
            })

        order = TransactionOrder.objects.get(id=object_id)
        info = u''
        if not order.invoice_status == InvoiceStatus.INVOICE_FINISHED or not order.ticket_status == TicketStatus.TICKET_CHECKOUT:
            info = u'该贴现服务尚有发票或汇票状态未完成，<a href="/transaction/transactionorder/%s">点击返回</a>' % order.id
        else:
            operation_list = TransactionOperation.objects.filter(transaction_id=order.id).all()
            for op in operation_list:
                if op.status != OperationStatus.OPERATION_FINISHED:
                    info = u'该贴现服务尚有流程操作未完成，<a href="/transaction/transactionorder/%s">点击返回</a>' % order.id
                    break
        if info:
            return render_to_response("management/notify.html", {
                "info": info,
                "title": u'贴现服务尚未完成',
                'user': request.user,
            })
        else:
            order.status = TRANSACTION_DONE
            order.finish_time = datetime.datetime.now()
            order.save()

        return super(TransactionOrderAdmin, self).change_view(request,
                                                              object_id,
                                                              form_url,
                                                              extra_context)

    @transaction.atomic
    def add_invoice(self, request, object_id, form_url='', extra_context=None):
        invoices = Invoice.objects.filter(transaction_id=long(object_id))
        if invoices.count() > 0:
            return render_to_response("management/notify.html", {
                "info": u'<h2>该贴现服务已有发票信息，<a href="/admin/ticket/invoice/%s">点击查看</a></h2>' % invoices.all()[0].id,
                "title": u'发票已存在',
                'user': request.user,
            })

        user_profile = get_user_profile(request.user)
        group_type = None if user_profile is None else user_profile.grouptype

        if request.user.is_superuser or group_type == StaffType.ACCOUNTANT:
            self.inlines = [InvoiceAddInline]
            self.exclude = ['transaction_claim', 'finish_time', 'invoice', 'ticket']
            self.readonly_fields = [
                'ticket_number', 'receivable_enterprise', 'pay_enterprise',
                'ticket_bank', 'accept_bank', 'amount', 'type', 'fee',
                'invoice_status', 'ticket_status', 'status', 'create_time'
            ]
            extra_context = dict(title=u'贴现开具发票', )
        else:
            raise PermissionDenied

        if request.method == 'POST':
            result = super(TransactionOrderAdmin, self).change_view(request,
                                                                    object_id,
                                                                    form_url,
                                                                    extra_context)
            # 添加成功才会返回HttpResponseRedirect，验证失败返回TemplateResponse
            if isinstance(result, HttpResponseRedirect):
                # 重置对用户的提醒信息
                request._messages = FallbackStorage(request)
                self.message_user(request, u'发票开具成功', messages.SUCCESS)
                # return super(TransactionOrderAdmin, self).changelist_view(request, extra_context)
                invoice = Invoice.objects.get(transaction_id=long(object_id))
                return HttpResponseRedirect('/staff/ticket/invoice/%s/' % invoice.id)
        return super(TransactionOrderAdmin, self).change_view(request, object_id, form_url, extra_context)

    @transaction.atomic
    def send_invoice(self, request, object_id, form_url='', extra_context=None):
        '''
        寄出发票
        '''
        invoices = Invoice.objects.filter(transaction_id=long(object_id))
        if invoices.count() < 1:
            return HttpResponseNotFound(u'<h1>该贴现服务尚未开具发票</h1>')
        elif invoices[0].status == InvoiceStatus.INVOICE_FINISHED:
            return HttpResponseNotFound(u'<h1>该贴现服务的发票已经寄出</h1>')

        user_profile = get_user_profile(request.user)
        group_type = None if user_profile is None else user_profile.grouptype

        if request.user.is_superuser or group_type == StaffType.ACCOUNTANT:
            self.inlines = [InvoiceEditInline]
            self.exclude = ['transaction_claim', 'finish_time', 'invoice', 'ticket']
            self.readonly_fields = [
                'ticket_number', 'receivable_enterprise', 'pay_enterprise',
                'ticket_bank', 'accept_bank', 'amount', 'type', 'fee',
                'invoice_status', 'ticket_status', 'status', 'create_time'
            ]
            extra_context = dict(title=u'贴现开具发票', )
        else:
            raise PermissionDenied
        return super(TransactionOrderAdmin, self).change_view(request, object_id, form_url, extra_context)

    @transaction.atomic
    def add_ticket(self, request, object_id, form_url='', extra_context=None):
        tickets = TransactionTicket.objects.filter(transaction_id=long(object_id))
        if tickets.count() > 0:
            return render_to_response("management/notify.html", {
                "info": u'<h2>该贴现服务已有汇票信息，<a href="/admin/ticket/transactionticket/%s">点击查看</a></h2>' % tickets.all()[0].id,
                "title": u'汇票已存在',
                'user': request.user,
            })

        self.inlines = [TicketAddInline]
        self.exclude = ['transaction_claim', 'finish_time', 'invoice', 'ticket']
        self.readonly_fields = [
            'ticket_number', 'receivable_enterprise', 'pay_enterprise',
            'ticket_bank', 'accept_bank', 'amount', 'type', 'fee',
            'invoice_status', 'ticket_status', 'status', 'create_time'
        ]
        extra_context = dict(title=u'贴现汇票入库', )

        user_profile = get_user_profile(request.user)
        group_type = None if user_profile is None else user_profile.grouptype

        if request.user.is_superuser or group_type in (StaffType.TICKET_CONDUCTOR, StaffType.TICKET_DIRECTOR):
            pass
        else:
            raise PermissionDenied

        if request.method == 'POST':
            result = super(TransactionOrderAdmin, self).change_view(request,
                                                                    object_id,
                                                                    form_url,
                                                                    extra_context)
            # 添加成功才会返回HttpResponseRedirect，验证失败返回TemplateResponse
            if isinstance(result, HttpResponseRedirect):
                # 重置对用户的提醒信息
                request._messages = FallbackStorage(request)
                self.message_user(request, u'汇票记录已添加', messages.SUCCESS)
                ticket = TransactionTicket.objects.get(transaction_id=long(object_id))
                return HttpResponseRedirect('/admin/ticket/transactionticket/%s/' % ticket.id)

        return super(TransactionOrderAdmin, self).change_view(request,
                                                              object_id,
                                                              form_url,
                                                              extra_context)

    def save_related(self, request, form, formsets, change):
        super(TransactionOrderAdmin, self).save_related(request, form, formsets, change)

        user_profile = get_user_profile(request.user)
        group_type = None if user_profile is None else user_profile.grouptype
        # 增加发票时记录 invoicelog
        if request.path.find('/add_invoice') > 0 and group_type == StaffType.ACCOUNTANT:
            for formset in formsets:
                if formset.form.Meta.model is Invoice:
                    for inline_form in formset.forms:
                        # inline_form.instance.accountant = user_profile
                        invoice_log = InvoiceLog()
                        invoice_log.invoice_id = inline_form.instance.id
                        # invoices = Invoice.objects.filter(pk=inline_form.instance.id)
                        # invoice_log.before_status = invoices[0].status if invoices.count() > 0 else None
                        invoice_log.before_status = InvoiceStatus.INVOICE_UNLODGED
                        invoice_log.after_status = inline_form.instance.status
                        invoice_log.operator = user_profile
                        invoice_log.remarks = u'开具发票，发票号：%s' % inline_form.instance.number
                        invoice_log.save()
                formset.save()
        elif request.path.find('/send_invoice') > 0 and group_type == StaffType.ACCOUNTANT:
            # 寄出发票时记录 invoicelog
            for formset in formsets:
                if formset.form.Meta.model is Invoice:
                    for inline_form in formset.forms:
                        inline_form.instance.status = InvoiceStatus.INVOICE_FINISHED
                        invoice_log = InvoiceLog()
                        invoice_log.invoice_id = inline_form.instance.id
                        invoices = Invoice.objects.filter(pk=inline_form.instance.id)
                        invoice_log.before_status = invoices[0].status if invoices.count() > 0 else None
                        invoice_log.after_status = InvoiceStatus.INVOICE_FINISHED
                        invoice_log.instance.operator = user_profile
                        invoice_log.remarks = u'寄出发票，EMS单号：%s' % inline_form.instance.send_ems
                        invoice_log.save()
                formset.save()
        elif request.path.find('/add_ticket') > 0 and group_type in (StaffType.TICKET_CONDUCTOR, StaffType.TICKET_DIRECTOR):
            # 寄出发票时记录 invoicelog
            for formset in formsets:
                if formset.form.Meta.model is TransactionTicket:
                    for inline_form in formset.forms:
                        inline_form.instance.status = TicketStatus.TICKET_RECEIVED_PENDING \
                            if group_type == StaffType.TICKET_CONDUCTOR else TicketStatus.TICKET_RECEIVED
                        ticket_log = TicketLog()
                        ticket_log.ticket_id = inline_form.instance.id
                        ticket_log.before_status = TicketStatus.TICKET_UNRECEIVED
                        ticket_log.after_status = TicketStatus.TICKET_RECEIVED_PENDING \
                            if group_type == StaffType.TICKET_CONDUCTOR else TicketStatus.TICKET_RECEIVED
                        ticket_log.operator = user_profile
                        ticket_log.remarks = u'收到汇票，EMS单号：%s' % inline_form.instance.receive_ems
                        ticket_log.save()
                        # todo for TICKET_CONDUCTOR
                formset.save()


    @csrf_protect_m
    def changelist_view(self, request, extra_context=None):
        if request.user.is_superuser:
            self.list_filter = ['status', ]
            self.list_display = ['ticket_number', 'amount', 'fee', 'status']
            return super(TransactionOrderAdmin, self).changelist_view(request, extra_context)

        user_profile = get_user_profile(request.user)
        group_type = None if user_profile is None else user_profile.grouptype
        self.change_list_template = None

        # only for member user
        if group_type in MemberUserType.values:
            # self.list_display = ('ticket_number', 'receivable_enterprise', 'pay_enterprise', 'ticket_bank', 'accept_bank', 'amount', 'type', 'fee', 'status')
            self.list_filter = ['status', ]
            self.list_display = [
                'ticket_number', 'receivable_enterprise', 'pay_enterprise',
                'ticket_bank', 'accept_bank', 'amount', 'fee', 'invoice_status',
                'ticket_status', 'create_time'
            ]
            self.change_list_template = 'member/history_order_change_list.html'

            # todo restrict queryset 找出该单位参与的
        elif group_type in (StaffType.MARKET_MANAGER, StaffType.ZONE_SERVICE, StaffType.SERVICE_MANAGER, StaffType.ZONE_SERVICE, StaffType.TOP_MANAGER):
            # todo @zhangnan for staff
            self.change_list_template = 'management/change_list.html'

            self.list_filter = ['status', ]
            self.list_display = [
                'ticket_number', 'receivable_enterprise', 'pay_enterprise',
                'ticket_bank', 'accept_bank', 'amount', 'fee', 'invoice_status',
                'ticket_status', 'create_time'
            ]
        elif group_type == StaffType.ACCOUNTANT:
            self.list_filter = ['invoice_status', ]
            self.list_display = [
                'ticket_number', 'receivable_enterprise', 'pay_enterprise',
                'amount', 'fee', 'invoice_status', 'ticket_status',
                'create_time', 'add_invoice_link'
            ]

        elif group_type in (StaffType.TICKET_DIRECTOR, StaffType.TICKET_CONDUCTOR):
            self.list_filter = ['ticket_status', ]
            self.list_display = [
                'ticket_number', 'payee_enterprise', 'payer_enterprise',
                'ticket_bank_name', 'accept_bank_name', 'amount', 'fee',
                'invoice_status', 'ticket_status', 'create_time', 'add_ticket_link'
            ]
        else:
            raise PermissionDenied

        # todo move here's ui logic to template
        title = u'全部贴现服务订单'
        if u'status__exact' in request.GET:
            status = request.GET[u'status__exact'].lower()
            if status == TransactionStatus.TRANSACTION_DONE.lower():
                title = u'已完成的'
            elif status == TransactionStatus.TRANSACTION_PROCESSING.lower():
                title = u'进行中的'
            elif status == TransactionStatus.TRANSACTION_ABORT.lower():
                title = u'已作废的'

        extra_context = dict(
            title=title + u'贴现服务',
            user_profile=user_profile,
        )

        return super(TransactionOrderAdmin, self).changelist_view(request, extra_context)

    # =============================================== TICKET LINK =====================================================
    def add_ticket_link(self, obj):
        # return u'<a class="button" href="/admin/transaction/transactionorder/%s/add_ticket"><strong>收票</strong></a>' % obj.id
        if obj.ticket_status == TicketStatus.TICKET_UNRECEIVED:
            return u'<a class="button" href="/admin/transaction/transactionorder/%s/add_ticket"><strong>收票</strong></a>' % obj.id
        else:
            return u'已收票'

    add_ticket_link.allow_tags = True
    add_ticket_link.short_description = u'收票'

    def payee_enterprise(self, obj):
        return obj.receivable_enterprise.name

    payee_enterprise.allow_tags = True
    payee_enterprise.short_description = u'收款企业'

    def payer_enterprise(self, obj):
        return obj.pay_enterprise.name

    payer_enterprise.allow_tags = True
    payer_enterprise.short_description = u'付款企业'

    def ticket_bank_name(self, obj):
        return obj.ticket_bank.name

    ticket_bank_name.allow_tags = True
    ticket_bank_name.short_description = u'贴现银行'

    def accept_bank_name(self, obj):
        return obj.accept_bank.name

    accept_bank_name.allow_tags = True
    accept_bank_name.short_description = u'承兑银行'

    # =============================================== INVOICE LINK =====================================================
    def add_invoice_link(self, obj):
        if obj.invoice_status == InvoiceStatus.INVOICE_UNLODGED:
            return u'<a class="button" href="/admin/transaction/transactionorder/%s/add_invoice"><strong>发票开具</strong></a>' % obj.id
        else:
            return u'已开票'

    add_invoice_link.allow_tags = True
    add_invoice_link.short_description = u'发票开具'

    def send_invoice_link(self, obj):
        if obj.invoice_status == InvoiceStatus.INVOICE_UNLODGED:
            return u''
        elif obj.invoice_status == InvoiceStatus.INVOICE_LODGED:
            # invoice = Invoice.objects.get(transaction_id=obj.id)
            return u'<a class="button" href="/admin/transaction/transactionorder/%s/send_invoice"><strong>发票寄出</strong></a>' % obj.id
        elif obj.invoice_status == InvoiceStatus.INVOICE_ABORT:
            return u'已作废'
        elif obj.invoice_status == InvoiceStatus.INVOICE_FINISHED:
            invoice = Invoice.objects.get(transaction_id=obj.id)
            return u'<a href="/admin/ticket/invoice/%s"><strong>已寄出</strong></a>' % invoice.id

    send_invoice_link.allow_tags = True
    send_invoice_link.short_description = u'发票寄出'

    @transaction.atomic
    def change_view(self, request, object_id, form_url='', extra_context=None):
        self.exclude = ['transaction_claim', ]
        self.readonly_fields = []

        user_profile = get_user_profile(request.user)
        group_type = None if user_profile is None else user_profile.grouptype

        if request.user.is_superuser:
            self.inlines = [TicketFormerHolderAddInline, TransactionOperationEditInline]
            self.change_form_template = None
            return super(TransactionOrderAdmin, self).change_view(request,
                                                                  object_id,
                                                                  form_url,
                                                                  extra_context)

        order = TransactionOrder.objects.get(id=long(object_id))
        if order.status == TransactionStatus.TRANSACTION_PROCESSING:
            self.inlines = [TicketFormerHolderReadonlyInline]
            self.exclude = [
                'transaction_claim', 'finish_time', 'invoice', 'ticket'
            ]
            self.readonly_fields = [
                'ticket_number', 'receivable_enterprise', 'pay_enterprise',
                'ticket_bank', 'accept_bank', 'amount', 'type', 'fee', 'status',
                'create_time', 'invoice_status', 'ticket_status'
            ]
        elif order.status == TransactionStatus.TRANSACTION_DONE:
            self.inlines = [TicketFormerHolderReadonlyInline]
            self.exclude = ['transaction_claim', ]
            self.readonly_fields = [
                'ticket_number', 'receivable_enterprise', 'pay_enterprise',
                'ticket_bank', 'accept_bank', 'amount', 'type', 'fee', 'status',
                'create_time', 'finish_time', 'invoice_status', 'ticket_status'
            ]

        if group_type in (MemberUserType.ENTERPRISE_CONTACTOR, MemberUserType.ENTERPRISE_OPERATOR):
            self.change_form_template = 'member/order_change_form_for_service.html'
            if user_profile.enterprise.id == order.receivable_enterprise.id:
                user_role = OperatorType.OPERATOR_RECEIVER
            elif user_profile.enterprise.id == order.pay_enterprise.id:
                user_role = OperatorType.OPERATOR_PAYER
        elif group_type in (MemberUserType.BANK_CONTACTOR, MemberUserType.BANK_OPERATOR):
            self.change_form_template = 'member/order_change_form_for_service.html'
            if user_profile.bank.id == order.ticket_bank.id:
                user_role = OperatorType.OPERATOR_TICKETBANK
            elif user_profile.bank.id == order.accept_bank.id:
                user_role = OperatorType.OPERATOR_ACCEPTBANK
        elif group_type in (StaffType.MARKET_MANAGER, StaffType.ZONE_SERVICE):
            self.change_form_template = 'management/order_change_form_for_service.html'
            user_role = OperatorType.OPERATOR_PLATFORM
        elif group_type in (StaffType.SERVICE_MANAGER, StaffType.ZONE_SERVICE):
            self.change_form_template = 'management/order_change_form_for_service.html'
            user_role = OperatorType.OPERATOR_PLATFORM
        elif group_type == StaffType.ACCOUNTANT:
            self.inlines = []
            self.change_form_template = None
            return super(TransactionOrderAdmin, self).change_view(request,
                                                                  object_id,
                                                                  form_url,
                                                                  extra_context)
        elif group_type in (StaffType.TICKET_DIRECTOR, StaffType.TICKET_CONDUCTOR):
            self.inlines = []
            self.change_form_template = None
            return super(TransactionOrderAdmin, self).change_view(request,
                                                                  object_id,
                                                                  form_url,
                                                                  extra_context)
        else:
            raise PermissionDenied

        operation_list = TransactionOperation.objects.filter(transaction_id=order.id).all()

        # If all the operations have been finished
        operation_alldone = False
        if all(op.status == OperationStatus.OPERATION_FINISHED for op in operation_list):
                operation_alldone = True

        extra_context = dict(operation_list=operation_list,
                             title=u'查看贴现服务',
                             OPERATION_UNACTIVATED=OperationStatus.OPERATION_UNACTIVATED,
                             OPERATION_ACTIVATED=OperationStatus.OPERATION_ACTIVATED,
                             OPERATION_PENDING=OperationStatus.OPERATION_PENDING,
                             OPERATION_FINISHED=OperationStatus.OPERATION_FINISHED,

                             MEMBER_BANK=MemberType.MEMBER_BANK,
                             MEMBER_ENTERPRISE=MemberType.MEMBER_ENTERPRISE,
                             MEMBER_PLATFORM=MemberType.MEMBER_PLATFORM,

                             OPERATOR_RECEIVER=OperatorType.OPERATOR_RECEIVER,
                             OPERATOR_PAYER=OperatorType.OPERATOR_PAYER,
                             OPERATOR_TICKETBANK=OperatorType.OPERATOR_TICKETBANK,
                             OPERATOR_ACCEPTBANK=OperatorType.OPERATOR_ACCEPTBANK,
                             OPERATOR_PLATFORM=OperatorType.OPERATOR_PLATFORM,

                             INVOICE_FINISHED=InvoiceStatus.INVOICE_FINISHED,
                             TICKET_CHECKOUT=TicketStatus.TICKET_CHECKOUT,
                             TRANSACTION_DONE=TransactionStatus.TRANSACTION_DONE,

                             operation_alldone=operation_alldone,
                             order=order,
                             user_role=user_role,
        )
        return super(TransactionOrderAdmin, self).change_view(request, object_id, form_url, extra_context)

    def get_queryset(self, request):
        qs = super(TransactionOrderAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        user_profile = get_user_profile(request.user)
        group_type = None if user_profile is None else user_profile.grouptype

        if group_type in (MemberUserType.BANK_CONTACTOR, MemberUserType.BANK_OPERATOR):
            return qs.filter(Q(ticket_bank=user_profile.bank_id) | Q(accept_bank=user_profile.bank_id)).order_by('-id')
        elif group_type in (MemberUserType.ENTERPRISE_OPERATOR, MemberUserType.ENTERPRISE_CONTACTOR):
            return qs.filter(Q(receivable_enterprise=user_profile.enterprise_id) | Q(pay_enterprise=user_profile.enterprise_id)).order_by('-id')
        elif isinstance(user_profile, Staff):
            return qs
        else:
            raise PermissionDenied


admin.site.register(TransactionOrder, TransactionOrderAdmin)
member_site.register(TransactionOrder, TransactionOrderAdmin)
management_site.register(TransactionOrder, TransactionOrderAdmin)

admin.site.register(TicketFormerHolder)


class TransactionOperationAdmin(admin.ModelAdmin):
    search_fields = ['transaction']

    def get_urls(self):
        urls = super(TransactionOperationAdmin, self).get_urls()
        my_urls = patterns('',
                           (r'^submit/$', self.submit),  # 提交贴现操作完成信息
                           (r'^(.+)/confirm/$', self.confirm),  # 客服审核完成改贴现操作
        )
        return my_urls + urls

    @transaction.atomic
    def submit(self, request, form_url='', extra_context=None):
        if not request.method == 'POST':
            raise PermissionDenied
        operation_id = long(request.POST['operation_id'])
        order_id = long(request.POST['order_id'])
        member_type = request.POST['member_type']
        member_id = long(request.POST['member_id'])

        user_profile = get_user_profile(request.user)
        group_type = None if user_profile is None else user_profile.grouptype

        # check for user permission
        if member_type == OperatorType.OPERATOR_PLATFORM:
            if not group_type in (StaffType.SERVICE_MANAGER, StaffType.ZONE_SERVICE):
                return HttpResponseNotFound(u'仅客服及客服经理能执行此操作')
        else:
            if member_type == OperatorType.OPERATOR_RECEIVER or member_type == OperatorType.OPERATOR_PAYER:
                if not hasattr(user_profile, 'enterprise') or not user_profile.enterprise.id == member_id:
                    return HttpResponseNotFound(u'你无权对该企业会员的贴现操作进行修改')
            elif member_type == OperatorType.OPERATOR_TICKETBANK or member_type == OperatorType.OPERATOR_ACCEPTBANK:
                member = Bank.objects.get(pk=member_id)
                if not hasattr(user_profile, 'bank') or not user_profile.bank.id == member_id:
                    return HttpResponseNotFound(u'你无权对该银行会员的贴现操作进行修改')

        # validation for operation
        operation = TransactionOperation.objects.get(pk=operation_id)
        if not operation.transaction_id == order_id:
            return HttpResponseNotFound(u'改贴现操作不属于该贴现订单')

        if operation.need_ems and 'ems_number_%s' % operation.id in request.POST:
            mail_number = request.POST['ems_number_%s' % operation.id]
            operation.ems_number = mail_number

        if operation.need_upload and 'upload_file_%s' % operation.id in request.FILES:
            upload_file = request.FILES['upload_file_%s' % operation.id]
            # todo upload
            operation.upload_file = upload_file

        if operation.need_confirm:
            operation.status = OperationStatus.OPERATION_PENDING
        else:
            operation.status = OperationStatus.OPERATION_FINISHED
            # 自动激活下一个贴现操作
            operation_list = TransactionOperation.objects.filter(transaction_id=operation.transaction_id).order_by('sequence').all()
            for i in range(operation_list.count()):
                if operation.id == operation_list[i].id:
                    if i + 1 < operation_list.count():
                        op = operation_list[i + 1]
                        op.status = OperationStatus.OPERATION_ACTIVATED
                        op.save()
                        break

        operation.operator_user = request.user
        operation.finish_time = datetime.datetime.now()
        operation.save()

        return HttpResponseRedirect('/admin/transaction/transactionorder/%s/' % order_id)

    @transaction.atomic
    def confirm(self, request, object_id, form_url='', extra_context=None):
        user_profile = get_user_profile(request.user)
        group_type = None if user_profile is None else user_profile.grouptype

        if not group_type in (StaffType.SERVICE_MANAGER, StaffType.ZONE_SERVICE):
            return HttpResponseNotFound(u'仅客服及客服经理能执行此操作')

        operation = TransactionOperation.objects.get(pk=object_id)
        if not operation.status == OperationStatus.OPERATION_PENDING:
            return HttpResponseNotFound(u'贴现流程状态必须是待审核')

        operation.status = OperationStatus.OPERATION_FINISHED
        operation.confirm_service = user_profile
        # operation.finish_time = datetime.datetime.now()
        # todo 审核时间
        operation.save()
        # 激活下一个贴现操作
        operation_list = TransactionOperation.objects.filter(
            transaction_id=operation.transaction_id,
            status=OperationStatus.OPERATION_UNACTIVATED
        ).order_by('sequence').all()
        if operation_list.count() > 0:
            for op in operation_list:
                op.status = OperationStatus.OPERATION_ACTIVATED
                op.save()
                break

        return HttpResponseRedirect('/admin/transaction/transactionorder/%s/' % operation.transaction_id)

    def get_queryset(self, request):
        qs = super(TransactionOperationAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        else:
            raise PermissionDenied


member_site.register(TransactionOperation, TransactionOperationAdmin)

management_site.register(TransactionOperation, TransactionOperationAdmin)

admin.site.register(TransactionOperation, TransactionOperationAdmin)


