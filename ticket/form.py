#coding=utf-8

from django.utils.deconstruct import deconstructible
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from django.contrib import admin
from django.forms import ModelForm
from django import forms
from django.db.models import Q
from django.contrib.auth.models import User, Group
from django.forms.models import BaseInlineFormSet

from ticket.models import *
from utils.constants import *
from member.models import Bank, Enterprise


class InvoiceAddInlineFormset(BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        super(InvoiceAddInlineFormset, self).__init__(*args, **kwargs)

    # 为了传参TransactionClaim的id给TransactionOrder Inline，特意重载
    @property
    def empty_form(self):
        form = self.form(
            auto_id=self.auto_id,
            prefix=self.add_prefix('__prefix__'),
            empty_permitted=True,
            fee=self.instance.fee,
        )
        self.add_fields(form, None)
        return form

    # 为了传参TransactionClaim的id给TransactionOrder Inline，特意重载
    def _construct_form(self, i, **kwargs):
        """
        Instantiates and returns the i-th form instance in a formset.
        """
        defaults = {
            'auto_id': self.auto_id,
            'prefix': self.add_prefix(i),
            'error_class': self.error_class,
            'fee': self.instance.fee,
        }
        if self.is_bound:
            defaults['data'] = self.data
            defaults['files'] = self.files
        if self.initial and 'initial' not in kwargs:
            try:
                defaults['initial'] = self.initial[i]
            except IndexError:
                pass
        # Allow extra forms to be empty, unless they're part of
        # the minimum forms.
        if i >= self.initial_form_count() and i >= self.min_num:
            defaults['empty_permitted'] = True
        defaults.update(kwargs)
        form = self.form(**defaults)
        self.add_fields(form, i)
        return form


class InvoiceAddForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        fee = kwargs.pop('fee') if 'fee' in kwargs else None
        super(InvoiceAddForm, self).__init__(*args, **kwargs)
        # 限制开票经理的选项只有区域市场经理和市场部总经理
        mm = Group.objects.get(id=StaffType.MARKET_MANAGER)
        zm = Group.objects.get(id=StaffType.ZONE_MARKET)
        # staffs = Staff.objects.filter(user__groups__in=[zm, mm]).all()
        self.fields['market_manager'].queryset = Staff.objects.filter(user__groups__in=[zm, mm])
        self.fields['amount'].initial = fee


class InvoiceAddInline(admin.StackedInline):
    model = Invoice
    extra = 1
    max_num = 1
    can_delete = False
    exclude = ['finish_time', 'status', 'create_time', 'send_ems']
    verbose_name = u'发票'
    verbose_name_plural = u'发票开具'
    form = InvoiceAddForm
    formset = InvoiceAddInlineFormset


class InvoiceEditInline(admin.StackedInline):
    model = Invoice
    extra = 1
    max_num = 1
    can_delete = False
    exclude = ['finish_time']
    readonly_fields = ['number', 'amount', 'market_manager', 'status', 'create_time']
    verbose_name = u'发票'
    verbose_name_plural = u'发票寄出'


class InvoiceReadonlyInline(admin.StackedInline):
    model = Invoice
    extra = 1
    max_num = 1
    can_delete = False
    readonly_fields = ['number', 'amount', 'market_manager', 'status', 'create_time', 'finish_time']
    exclude = ['create_time', ]
    verbose_name = u'贴现发票'
    verbose_name_plural = u'查看贴现发票'


class InvoiceLogInline(admin.TabularInline):
    model = InvoiceLog
    extra = 0
    can_delete = False
    max_num = 0
    readonly_fields = ['before_status', 'after_status', 'remarks', 'operator', 'create_time']
    exclude = ['invoice']
    verbose_name = u'发票状态变更'
    verbose_name_plural = u'发票状态变更记录'


# ============================================= TICKET =================================================

class TicketAddInlineFormset(BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        super(TicketAddInlineFormset, self).__init__(*args, **kwargs)

    # 为了传参TransactionClaim的id给TransactionOrder Inline，特意重载
    @property
    def empty_form(self):
        form = self.form(
            auto_id=self.auto_id,
            prefix=self.add_prefix('__prefix__'),
            empty_permitted=True,
            ticket_bank_id=self.instance.ticket_bank.id,
            ticket_number=self.instance.ticket_number,
            amount=self.instance.amount,
        )
        self.add_fields(form, None)
        return form

    # 为了传参TransactionClaim的id给TransactionOrder Inline，特意重载
    def _construct_form(self, i, **kwargs):
        """
        Instantiates and returns the i-th form instance in a formset.
        """
        defaults = {
            'auto_id': self.auto_id,
            'prefix': self.add_prefix(i),
            'error_class': self.error_class,
            'ticket_bank_id': self.instance.ticket_bank.id,
            'ticket_number': self.instance.ticket_number,
            'amount': self.instance.amount,
        }
        if self.is_bound:
            defaults['data'] = self.data
            defaults['files'] = self.files
        if self.initial and 'initial' not in kwargs:
            try:
                defaults['initial'] = self.initial[i]
            except IndexError:
                pass
        # Allow extra forms to be empty, unless they're part of
        # the minimum forms.
        if i >= self.initial_form_count() and i >= self.min_num:
            defaults['empty_permitted'] = True
        defaults.update(kwargs)
        form = self.form(**defaults)
        self.add_fields(form, i)
        return form


class TicketAddForm(forms.ModelForm):
    class Meta:
        model = TransactionTicket
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        ticket_bank_id = kwargs.pop('ticket_bank_id') if 'ticket_bank_id' in kwargs else None
        ticket_number = kwargs.pop('ticket_number') if 'ticket_number' in kwargs else None
        amount = kwargs.pop('amount') if 'amount' in kwargs else None
        super(TicketAddForm, self).__init__(*args, **kwargs)
        self.fields['ticket_bank'].widget.attrs.update({'disabled': 'true'})
        self.fields['ticket_bank'].queryset = Bank.objects.filter(id=ticket_bank_id)
        self.fields['ticket_bank'].empty_label = None
        self.fields['ticket_bank'].empty_value = []
        self.fields['number'].initial = ticket_number
        self.fields['amount'].initial = amount


class TicketAddInline(admin.StackedInline):
    model = TransactionTicket
    extra = 1
    max_num = 1
    can_delete = False
    exclude = ['finish_time', 'status', 'send_ems']
    verbose_name = u'汇票'
    verbose_name_plural = u'汇票入库'
    form = TicketAddForm
    formset = TicketAddInlineFormset


class TicketLogInline(admin.TabularInline):
    model = TicketLog
    extra = 0
    can_delete = False
    max_num = 0
    readonly_fields = ['before_status', 'after_status', 'remarks', 'operator', 'create_time']
    exclude = ['ticket']
    verbose_name = u'汇票状态变更'
    verbose_name_plural = u'汇票状态变更记录'



