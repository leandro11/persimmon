#coding=utf-8

from django.contrib import admin
from django.conf.urls import patterns
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from django.core.exceptions import PermissionDenied
from django.http import Http404, HttpResponseNotFound
from django.db import transaction
from django.contrib.admin.utils import unquote

from utils.user import get_user_profile
from utils.constants import *
from ticket.form import *
from ticket.models import *
from management.sites import site as management_site

csrf_protect_m = method_decorator(csrf_protect)


class InvoiceAdmin(admin.ModelAdmin):
    search_fields = ['transaction', 'number']
    # list_display = ['name', 'fee']
    search_fields = ['number']

    def get_urls(self):
        urls = super(InvoiceAdmin, self).get_urls()
        my_urls = patterns('',
                           (r'^(.+)/send/$', self.send_view),  # 寄出发票
        )
        return my_urls + urls

    def add_view(self, request, form_url='', extra_context=None):
        self.inlines = []
        self.readonly_fields = []
        self.exclude = ['status', 'finish_time']
        return super(InvoiceAdmin, self).add_view(request, form_url, extra_context)

    @transaction.atomic
    def send_view(self, request, object_id, form_url='', extra_context=None):
        '''
        寄出发票
        '''
        if Invoice.objects.get(pk=long(object_id)).status == INVOICE_FINISHED:
            return HttpResponseNotFound(u'<h1>该贴现服务的发票已经寄出</h1>')

        user_profile = get_user_profile(request.user)
        group_name = None if user_profile is None else user_profile.groupname

        if request.user.is_superuser:
            self.exclude = []
            self.readonly_fields = []
        elif group_name in (ACCOUNTANT, TOP_MANAGER):
            self.exclude = ['finish_time', ]
            self.readonly_fields = ['number', 'amount', 'transaction', 'market_manager', 'status', 'create_time']
            # self.inlines = [InvoiceEditInline]
            # self.exclude = ['transaction_claim', 'finish_time', 'invoice', 'ticket']
            # self.readonly_fields = ['ticket_number', 'receivable_enterprise', 'pay_enterprise', 'ticket_bank', 'accept_bank', 'amount', 'type', 'fee', 'invoice_status',
            #                         'ticket_status', 'status', 'create_time']
            extra_context = dict(title=u'贴现发票寄出', )
        else:
            raise PermissionDenied

        if request.method == 'POST':
            # if not obj.send_ems:
            #     return HttpResponseNotFound(u'<h1>ems单号不能为空</h1>')
            # todo 检查ems单号不能为空
            pass
        self.change_form_template = 'management/change_form.html'
        return super(InvoiceAdmin, self).change_view(request, object_id, form_url, extra_context)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        invoice = Invoice.objects.get(pk=long(object_id))
        if invoice.status == INVOICE_FINISHED:
            self.readonly_fields = ['transaction', 'number', 'amount', 'market_manager', 'send_ems', 'status', 'create_time', 'finish_time']
            self.exclude = []
        else:
            self.readonly_fields = ['transaction', 'number', 'amount', 'market_manager', 'send_ems', 'status', 'create_time']
            self.exclude = ['finish_time']
        self.inlines = [InvoiceLogInline, ]
        return super(InvoiceAdmin, self).change_view(request, object_id, form_url, extra_context)

    @csrf_protect_m
    def changelist_view(self, request, extra_context=None):
        if request.user.is_superuser:
            self.list_filter = ['status', ]
            self.list_display = ['number', 'amount', 'transaction_link', 'market_manager_link', 'send_ems', 'create_time', 'send_invoice_link']
            return super(InvoiceAdmin, self).changelist_view(request, extra_context)

        user_profile = get_user_profile(request.user)
        group_name = None if user_profile is None else user_profile.groupname

        if group_name == ACCOUNTANT:
            self.list_filter = ['status', ]
            self.list_display = ['number', 'amount', 'transaction_link', 'market_manager_link', 'send_ems', 'create_time', 'send_invoice_link']
        elif group_name == TOP_MANAGER:
            self.list_filter = ['status', ]
            self.list_display = ['number', 'amount', 'transaction_link', 'market_manager_link', 'send_ems', 'create_time', 'send_invoice_link']
        else:
            raise PermissionDenied
        return super(InvoiceAdmin, self).changelist_view(request, extra_context)


    def save_model(self, request, obj, form, change):
        user_profile = get_user_profile(request.user)
        group_name = None if user_profile is None else user_profile.groupname
        if request.path.find('/send') > 0 and group_name == ACCOUNTANT:
            obj.status = INVOICE_FINISHED
            invoice_log = InvoiceLog()
            invoice_log.invoice_id = obj.id
            invoice_log.before_status = Invoice.objects.get(pk=obj.id).status
            invoice_log.after_status = INVOICE_FINISHED
            invoice_log.operator = user_profile
            invoice_log.remarks = u'寄出发票，EMS单号：：%s' % obj.send_ems
            invoice_log.save()
        super(InvoiceAdmin, self).save_model(request, obj, form, change)


admin.site.register(Invoice, InvoiceAdmin)
admin.site.register(InvoiceLog)
management_site.register(Invoice, InvoiceAdmin)


class TransactionTicketAdmin(admin.ModelAdmin):
    search_fields = ['transaction', 'number']

    def add_view(self, request, form_url='', extra_context=None):
        self.readonly_fields = []
        self.exclude = ['status', 'ticket_bank', 'finish_time']
        return super(TransactionTicketAdmin, self).add_view(request, form_url, extra_context)

    def get_urls(self):
        urls = super(TransactionTicketAdmin, self).get_urls()
        my_urls = patterns('',
                           (r'^(.+)/checkin/$', self.checkin_view),  # 汇票出库界面
        )
        return my_urls + urls

    def checkin_view(self, request, object_id, form_url='', extra_context=None):
        user_profile = get_user_profile(request.user)
        group_type = None if user_profile is None else user_profile.grouptype

        if group_type not in (StaffType.TICKET_CONDUCTOR, StaffType.TICKET_DIRECTOR):
            raise PermissionDenied

        if request.method == 'POST':
            # send_ems不能为空
            if 'send_ems' in request.POST and not request.POST['send_ems'].strip():
                return HttpResponseNotFound(u'出票快递单号不能为空')

        self.readonly_fields = [
            'ticket_bank', 'number', 'amount', 'receive_ems',
            'status', 'create_time', 'finish_time'
        ]
        self.exclude = ['transaction', ]
        self.inlines = []
        return super(TransactionTicketAdmin, self).change_view(request,
                                                               object_id,
                                                               form_url,
                                                               extra_context)

    def save_model(self, request, obj, form, change):
        # 将状态置为入库待核 TICKET_CHECKIN_PENDING
        if request.method == 'POST' and request.path.find('/checkin') > 0:
            ticketlog = TicketLog()
            ticketlog.ticket = obj
            ticketlog.before_status = obj.status
            ticketlog.after_status = TicketStatus.TICKET_CHECKIN_PENDING
            ticketlog.remarks = u'入库待审核，入库EMS单号：%s' % obj.send_ems
            ticketlog.operator = get_user_profile(request.user)
            ticketlog.save()
            obj.status = TicketStatus.TICKET_CHECKIN_PENDING
        super(TransactionTicketAdmin, self).save_model(request, obj, form, change)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        if request.user.is_superuser:
            self.inlines = [TicketLogInline, ]
            return super(TransactionTicketAdmin, self).change_view(request,
                                                                   object_id,
                                                                   form_url,
                                                                   extra_context)
        self.readonly_fields = [
            'number', 'ticket_bank', 'amount', 'receive_ems', 'send_ems',
            'status', 'create_time', 'finish_time'
        ]
        self.exclude = ['transaction']
        self.inlines = [TicketLogInline, ]

        user_profile = get_user_profile(request.user)
        group_type = None if user_profile is None else user_profile.grouptype

        if group_type in (StaffType.TICKET_CONDUCTOR, StaffType.TICKET_DIRECTOR, StaffType.TOP_MANAGER):
            pass
        else:
            return Http404

        self.change_list_template = 'management/change_form.html'
        return super(TransactionTicketAdmin, self).change_view(request,
                                                               object_id,
                                                               form_url,
                                                               extra_context)

    @csrf_protect_m
    def changelist_view(self, request, extra_context=None):
        if request.user.is_superuser:
            self.list_filter = ['status', ]
            self.list_display = [
                'number', 'transaction_link', 'ticket_bank_link', 'amount',
                'receive_ems', 'send_ems', 'create_time', 'receive_ticket_link',
                'verify_ticket_link', 'checkin_link', 'checkout_link'
            ]
            return super(TransactionTicketAdmin, self).changelist_view(request, extra_context)

        user_profile = get_user_profile(request.user)
        group_type = None if user_profile is None else user_profile.grouptype

        if group_type == StaffType.TICKET_CONDUCTOR:
            self.list_filter = []
            self.list_display = [
                'number', 'transaction_link', 'ticket_bank_link', 'amount',
                'receive_ems', 'send_ems', 'create_time', 'receive_ticket_link',
                'verify_ticket_link', 'checkin_link', 'checkout_link'
            ]
            if 'verify_pending' in request.GET and request.GET['verify_pending'].isdigit():
                ticket = TransactionTicket.objects.get(pk=long(request.GET['verify_pending']))
                ticketlog = TicketLog()
                ticketlog.ticket = ticket
                ticketlog.before_status = ticket.status
                ticketlog.after_status = TicketStatus.TICKET_VERIFIED_PENDING
                ticketlog.remarks = u'验票操作，等待审核'
                ticketlog.operator = user_profile
                ticketlog.save()
                ticket.status = TicketStatus.TICKET_VERIFIED_PENDING
                ticket.save()

            if 'checkout_pending' in request.GET and request.GET['checkout_pending'].isdigit():
                ticket = TransactionTicket.objects.get(pk=long(request.GET['checkout_pending']))
                ticketlog = TicketLog()
                ticketlog.ticket = ticket
                ticketlog.before_status = ticket.status
                ticketlog.after_status = TicketStatus.TICKET_CHECKOUT_PENDING
                ticketlog.remarks = u'出库操作，等待审核'
                ticketlog.operator = user_profile
                ticketlog.save()
                ticket.status = TicketStatus.TICKET_CHECKOUT_PENDING
                ticket.save()

        elif group_type == StaffType.TICKET_DIRECTOR:
            self.list_filter = []
            self.list_display = [
                'number', 'transaction_link', 'ticket_bank_link', 'amount',
                'receive_ems', 'send_ems', 'create_time', 'receive_ticket_link_director',
                'verify_ticket_link_director', 'checkin_link_director', 'checkout_link_director'
            ]
            if 'receive_confirm' in request.GET and request.GET['receive_confirm'].isdigit():
                ticket = TransactionTicket.objects.get(pk=long(request.GET['receive_confirm']))
                ticketlog = TicketLog()
                ticketlog.ticket = ticket
                ticketlog.before_status = ticket.status
                ticketlog.after_status = TicketStatus.TICKET_RECEIVED
                ticketlog.remarks = u'收票审核通过'
                ticketlog.operator = user_profile
                ticketlog.save()
                ticket.status = TicketStatus.TICKET_RECEIVED
                ticket.save()

            if 'verify_confirm' in request.GET and request.GET['verify_confirm'].isdigit():
                ticket = TransactionTicket.objects.get(pk=long(request.GET['verify_confirm']))
                ticketlog = TicketLog()
                ticketlog.ticket = ticket
                ticketlog.before_status = ticket.status
                ticketlog.after_status = TicketStatus.TICKET_VERIFIED
                ticketlog.remarks = u'验票审核通过'
                ticketlog.operator = user_profile
                ticketlog.save()
                ticket.status = TicketStatus.TICKET_VERIFIED
                ticket.save()

            if 'checkin_confirm' in request.GET and request.GET['checkin_confirm'].isdigit():
                ticket = TransactionTicket.objects.get(pk=long(request.GET['checkin_confirm']))
                ticketlog = TicketLog()
                ticketlog.ticket = ticket
                ticketlog.before_status = ticket.status
                ticketlog.after_status = TicketStatus.TICKET_CHECKIN
                ticketlog.remarks = u'入库审核通过'
                ticketlog.operator = user_profile
                ticketlog.save()
                ticket.status = TicketStatus.TICKET_CHECKIN
                ticket.save()

            if 'checkout_confirm' in request.GET and request.GET['checkout_confirm'].isdigit():
                ticket = TransactionTicket.objects.get(pk=long(request.GET['checkout_confirm']))
                ticketlog = TicketLog()
                ticketlog.ticket = ticket
                ticketlog.before_status = ticket.status
                ticketlog.after_status = TicketStatus.TICKET_CHECKOUT
                ticketlog.remarks = u'出库审核通过'
                ticketlog.operator = user_profile
                ticketlog.save()
                ticket.status = TicketStatus.TICKET_CHECKOUT
                ticket.save()
        else:
            raise PermissionDenied
        self.change_list_template = 'management/change_list.html'
        return super(TransactionTicketAdmin, self).changelist_view(request, extra_context)


admin.site.register(TransactionTicket, TransactionTicketAdmin)
management_site.register(TransactionTicket, TransactionTicketAdmin)
admin.site.register(TicketLog)




