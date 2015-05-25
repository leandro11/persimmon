#coding=utf-8

from django.db import models

from transaction.models import *
from utils.constants import *
from utils.constants import (
    InvoiceStatus, INVOICE_STATUS, INVOICE_STATUS2, TicketStatus,
    TICKET_STATUS, TICKET_STATUS2, StaffType)

from ticket.ticket_status import (
    UnreceivedState, ReceivedPendingState, ReceivedState, CheckinPendingState,
    CheckinState, VerifiedPendingState, VerifiedState, CheckoutPendingState,
    CheckoutState)
from ticket.invoice_status import (
    UnlodgedState, LodgedState, FinishedState, AbortState)


class Invoice(models.Model):
    '''
    发票
    '''
    transaction = models.OneToOneField(TransactionOrder, blank=False, null=False, verbose_name=u'贴现服务订单', related_name='invoice')
    number = models.CharField(unique=True, max_length=50, blank=False, null=False, verbose_name=u'发票单号')
    amount = models.DecimalField(max_digits=11, decimal_places=2, blank=False, null=False, verbose_name=u'金额')
    market_manager = models.ForeignKey(Staff, related_name='invoice_market_manager', blank=False, null=False, verbose_name=u'开票经理')
    # accountant = models.ForeignKey(Staff, related_name='invoice_accountant', blank=True, null=True, verbose_name=u'开票会计')
    send_ems = models.CharField(unique=True, max_length=50, blank=True, null=True, verbose_name=u'寄出EMS')
    status = models.CharField(max_length=30, choices=INVOICE_STATUS, default=InvoiceStatus.INVOICE_LODGED, verbose_name=u'操作状态')
    create_time = models.DateTimeField(auto_now_add=True, editable=True, verbose_name=u'创建时间')
    finish_time = models.DateTimeField(blank=True, null=True, editable=True, verbose_name=u'完成时间', default=None)

    # current state of invoice
    state = None

    class Meta:
        verbose_name = u'发票'
        verbose_name_plural = u'发票'

    def __unicode__(self):
        return self.number

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        #同步更改transaction order中的invoice_status
        super(Invoice, self).save(force_insert, force_update, using, update_fields)
        order = TransactionOrder.objects.get(id=self.transaction_id)
        order.invoice_status = self.status
        order.save()

    def market_manager_link(self):
        market_manager = Staff.objects.get(pk=self.market_manager_id)
        return u'<a href="/staff/management/staff/%s"><strong>%s</strong></a>' % (market_manager.id, market_manager.name)

    market_manager_link.allow_tags = True
    market_manager_link.short_description = u'开票市场经理'

    def transaction_link(self):
        transaction = TransactionOrder.objects.get(pk=self.transaction_id)
        return u'<a href="/staff/transaction/transactionorder/%s"><strong>%s</strong></a>' % (transaction.id, transaction.ticket_number)

    transaction_link.allow_tags = True
    transaction_link.short_description = u'贴现服务订单'

    def set_state(self, state):
        self.state = state

    def create_state(self):
        if self.status == InvoiceStatus.INVOICE_UNLODGED:
            self.set_state(UnlodgedState(self))
        elif self.status == InvoiceStatus.INVOICE_LODGED:
            self.set_state(LodgedState(self))
        elif self.status == InvoiceStatus.INVOICE_FINISHED:
            self.set_state(FinishedState(self))
        else:
            self.set_state(AbortState(self))

    def show_link(self):
        self.create_state()
        return self.state.show_link()

    show_link.allow_tags = True
    show_link.short_description = u'发票寄出'

    def send(self):
        self.create_state()
        self.state.send()


# 记录发票状态变更记录
class InvoiceLog(models.Model):
    invoice = models.ForeignKey(Invoice, blank=False, null=False, verbose_name=u'发票')
    before_status = models.CharField(max_length=30, choices=INVOICE_STATUS2, default=InvoiceStatus.INVOICE_UNLODGED, blank=False, null=False, verbose_name=u'变更前状态')
    after_status = models.CharField(max_length=30, choices=INVOICE_STATUS2, blank=False, null=False, verbose_name=u'变更后状态')
    remarks = models.CharField(max_length=300, blank=True, null=True, verbose_name=u'备注')
    operator = models.ForeignKey(Staff, blank=False, null=False, verbose_name=u'执行人')
    create_time = models.DateTimeField(auto_now_add=True, editable=True, verbose_name=u'操作时间')

    class Meta:
        verbose_name = u'发票变更'
        verbose_name_plural = u'发票变更记录'

    def __unicode__(self):
        return u'%s->%s' % (self.get_before_status_display(), self.get_after_status_display())


# ======================================================================================================================
class TransactionTicket(models.Model):
    '''
    汇票
    '''
    transaction = models.OneToOneField(TransactionOrder, blank=False, null=False, verbose_name=u'贴现服务订单', related_name='ticket')
    ticket_bank = models.ForeignKey(Bank, blank=False, null=False, verbose_name=u'贴现银行')
    number = models.CharField(unique=True, max_length=50, blank=False, null=False, verbose_name=u'汇票号')
    amount = models.DecimalField(max_digits=11, decimal_places=2, blank=False, null=False, verbose_name=u'金额')
    receive_ems = models.CharField(max_length=50, blank=False, null=False, verbose_name=u'入票快递')
    send_ems = models.CharField(max_length=50, blank=True, null=True, verbose_name=u'出票快递')
    status = models.CharField(max_length=30, choices=TICKET_STATUS, default=TicketStatus.TICKET_RECEIVED_PENDING, verbose_name=u'操作状态')
    # conductor = models.ForeignKey(Staff, related_name='conductor', blank=True, null=True, verbose_name=u'核票员')
    # director = models.ForeignKey(Staff, related_name='director', blank=True, null=True, verbose_name=u'票据主管')
    create_time = models.DateTimeField(auto_now_add=True, editable=True, verbose_name=u'收票时间')
    finish_time = models.DateTimeField(blank=True, null=True, editable=True, verbose_name=u'完成时间', default=None)

    # current state of ticket
    state = None

    class Meta:
        verbose_name = u'汇票'
        verbose_name_plural = u'汇票'

    def __unicode__(self):
        return self.number

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        #同步更改transaction order中的ticket_status
        super(TransactionTicket, self).save(force_insert, force_update, using, update_fields)
        order = TransactionOrder.objects.get(id=self.transaction_id)
        order.ticket_status = self.status
        order.save()

    def transaction_link(self):
        transaction = TransactionOrder.objects.get(pk=self.transaction_id)
        return u'<a href="/staff/transaction/transactionorder/%s"><strong>%s->%s</strong></a>' % (
            transaction.id, transaction.receivable_enterprise.name, transaction.pay_enterprise.name)

    transaction_link.allow_tags = True
    transaction_link.short_description = u'贴现服务订单'

    def set_state(self, state):
        self.state = state

    def create_state(self):
        if self.status == TicketStatus.TICKET_UNRECEIVED:
            self.set_state(UnreceivedState(self))
        elif self.status == TicketStatus.TICKET_RECEIVED_PENDING:
            self.set_state(ReceivedPendingState(self))
        elif self.status == TicketStatus.TICKET_RECEIVED:
            self.set_state(ReceivedState(self))
        elif self.status == TicketStatus.TICKET_CHECKIN_PENDING:
            self.set_state(CheckinPendingState(self))
        elif self.status == TicketStatus.TICKET_CHECKIN:
            self.set_state(CheckinState(self))
        elif self.status == TicketStatus.TICKET_VERIFIED_PENDING:
            self.set_state(VerifiedPendingState(self))
        elif self.status == TicketStatus.TICKET_VERIFIED:
            self.set_state(VerifiedState(self))
        elif self.status == TicketStatus.TICKET_CHECKOUT_PENDING:
            self.set_state(CheckoutPendingState(self))
        else:
            # Status is Checkout State
            self.set_state(CheckoutState(self))

    def receive_tickets(self):
        self.create_state()
        self.state.receive_tickets()

    def confirm_receive_tickets(self):
        self.create_state()
        self.state.confirm_receive_tickets()

    def verify_tickets(self):
        self.create_state()
        self.state.verify_tickets()

    def confirm_verify_tickets(self):
        self.create_state()
        self.state.confirm_verify_tickets()

    def checkin_tickets(self):
        self.create_state()
        self.state.checkin_tickets()

    def confirm_checkin_tickets(self):
        self.create_state()
        self.state.confirm_checkin_tickets()

    def checkout_tickets(self):
        self.create_state()
        self.state.checkout_tickets()

    def confirm_checkout_tickets(self):
        self.create_state()
        self.state.confirm_checkout_tickets()

    def show_conductor_link(self):
        self.create_state()
        return self.state.show_link()


    def show_director_link(self):
        self.create_state()
        return self.state.show_link(role=StaffType.TICKET_DIRECTOR)


    def ticket_bank_link(self):
        ticket_bank = Bank.objects.get(pk=self.ticket_bank_id)
        return u'<a href="/staff/member/bank/%s"><strong>%s</strong></a>' % (ticket_bank.id, ticket_bank.name)

    ticket_bank_link.allow_tags = True
    ticket_bank_link.short_description = u'贴现银行'


# 记录发票状态变更记录
class TicketLog(models.Model):
    ticket = models.ForeignKey(TransactionTicket, blank=False, null=False, verbose_name=u'汇票')
    before_status = models.CharField(max_length=30, choices=TICKET_STATUS2, blank=False, null=False, verbose_name=u'变更前状态')
    after_status = models.CharField(max_length=30, choices=TICKET_STATUS2, blank=False, null=False, verbose_name=u'变更后状态')
    remarks = models.CharField(max_length=300, blank=True, null=True, verbose_name=u'操作状态')
    operator = models.ForeignKey(Staff, blank=False, null=False, verbose_name=u'执行人')
    create_time = models.DateTimeField(auto_now_add=True, editable=True, verbose_name=u'操作时间')

    class Meta:
        verbose_name = u'汇票变更'
        verbose_name_plural = u'汇票变更记录'

    def __unicode__(self):
        return u'%s->%s' % (self.get_before_status_display(), self.get_after_status_display())

