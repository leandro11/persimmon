#coding=utf-8
from django.shortcuts import get_object_or_404, render_to_response, render, redirect
from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.forms.models import modelformset_factory, inlineformset_factory
from django.forms import ModelForm
from django.views.generic import CreateView, UpdateView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.template import RequestContext
from django.core.exceptions import NON_FIELD_ERRORS
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Q

from management.models import Staff
from management.auth import login, logout, logout_then_login, redirect_to_login
from transaction.models import (TransactionClaim, TransactionOrder, TRANSACTION_PROCESSING,
    TRANSACTION_DONE, TRANSACTION_ABORT, CLAIM_PENDING, CLAIM_PASSED, CLAIM_ABORT)
from member.models import (Enterprise, Bank, RegisterInvitationCode, MEMBER_ENABLED,
    MEMBER_PENDING, MEMBER_DISABLED, MEMBER_EXPIRED, CODE_ACTIVATED)
from utils.user import get_user_profile
from utils.constants import (
    StaffType, TICKET_RECEIVED_PENDING, TICKET_RECEIVED, TICKET_VERIFIED_PENDING, TICKET_VERIFIED,
    TICKET_CHECKIN_PENDING, TICKET_CHECKIN, TICKET_CHECKOUT_PENDING, TICKET_CHECKOUT,
    INVOICE_LODGED, INVOICE_FINISHED, INVOICE_UNLODGED, TICKET_UNRECEIVED)
from ticket.models import TransactionTicket, Invoice


csrf_protect_m = method_decorator(csrf_protect)


class StaffForm(ModelForm):
    class Meta:
        model = Staff
        fields = '__all__'

        error_messages = {
            NON_FIELD_ERRORS: {
                'unique_together': "%(model_name)s's %(field_labels)s are not unique.",
            }
        }


def register(request):
    staff_formset = modelformset_factory(
        Staff,
        exclude=('is_active', 'last_login', 'date_joined', 'user')
    )

    if request.method == 'POST':
        staff_formset = StaffForm(request.POST or None, request.FILES)
        return HttpResponse('123123')

    return render_to_response("management/staff_register.html", {
        "staff_formset": staff_formset,
        "title": u'工作人员注册',
    }, context_instance=RequestContext(request))


def main_view(request):
    if not request.user.is_authenticated():
        return redirect_to_login('/management/login')

    user_profile = get_user_profile(request.user)
    group_type = None if user_profile is None else user_profile.grouptype
    if group_type == StaffType.MARKET_MANAGER:  # 市场部总经理
        return zone_market_dashboard(request, user_profile)
    elif group_type == StaffType.ZONE_MARKET:  # 区域市场经理
        return zone_market_dashboard(request, user_profile)
    elif group_type == StaffType.SERVICE_MANAGER:  # 客服部总经理
        return zone_service_dashboard(request, user_profile)
    elif group_type == StaffType.ZONE_SERVICE:  # 区域客服
        return zone_service_dashboard(request, user_profile)
    elif group_type == StaffType.TICKET_DIRECTOR:  # 票据主管
        return ticket_director_dashboard(request, user_profile)
    elif group_type == StaffType.TICKET_CONDUCTOR:  # 核票员
        return ticket_conductor_dashboard(request, user_profile)
    elif group_type == StaffType.ACCOUNTANT:  # 会计
        return accountant_dashboard(request, user_profile)
    elif group_type == StaffType.TOP_MANAGER:  # 总经理
        pass
    else:
        # /management/login的接口只工作人员登陆
        logout(request)
        return HttpResponseRedirect('/management/login')
        # return redirect_to_login('/management/login')

    return HttpResponse('error： empty group')


 # 客服 dashboard
def zone_service_dashboard(request, user_profile):
    # different kinds of orders
    ongoing_orders = TransactionOrder.objects.filter(
        status=TRANSACTION_PROCESSING).order_by('-create_time')[:5]

    # Get different types of enterprise members
    pending_enterprises = Enterprise.objects.filter(
        status=MEMBER_PENDING).order_by('-create_date')[:5]

    # Get different types of bank members
    pending_banks = Bank.objects.filter(
        status=MEMBER_PENDING).order_by('-create_date')[:5]

    context = dict(
        user_id=user_profile.user.id,
        user_profile=user_profile,
        group_name=user_profile.groupname,
        title=u'%s管理后台' % user_profile.groupname,
        ongoing_orders=ongoing_orders,
        pending_enterprises=pending_enterprises,
        pending_banks=pending_banks,
    )
    return TemplateResponse(request, 'management/service_dashboard.html', context, current_app='1231')


 # 市场 dashboard
def zone_market_dashboard(request, user_profile):
    # Get pending claim for market staff
    pending_claim = TransactionClaim.objects.filter(
        status=CLAIM_PENDING).order_by('-create_time')[:5]

    # Get Enterprise customers, including service and referee
    enterprise_customers = Enterprise.objects.filter(
        # Q(referee_manager=user_profile.user) | Q(service_manager=user_profile.user),
        status=MEMBER_PENDING
    ).order_by('-create_date')[:5]

    # Get Bank customers, including service and referee
    bank_customers = Bank.objects.filter(
        # Q(service_manager=user_profile.user) | Q(referee_manager=user_profile.user),
        status=MEMBER_PENDING
    ).order_by('-create_date')[:5]

    context = dict(
        user_id=user_profile.user.id,
        user_profile=user_profile,
        group_name=user_profile.groupname,
        title=u'%s管理后台' % user_profile.groupname,
        pending_claim=pending_claim,
        enterprise_customers=enterprise_customers,
        bank_customers=bank_customers,
    )
    return TemplateResponse(request, 'management/market_dashboard.html', context, current_app='1231')


 # 核票员 dashboard
def ticket_conductor_dashboard(request, user_profile):
    # Get on going orders of transaction
    ongoing_orders = TransactionOrder.objects.filter(
        status=TRANSACTION_PROCESSING,
        ticket_status=TICKET_UNRECEIVED).order_by('-create_time')[:5]

    # Get ongoing type of tickets
    ongoing_tickets = TransactionTicket.objects.filter(
        Q(status=TICKET_RECEIVED) |
        Q(status=TICKET_VERIFIED) |
        Q(status=TICKET_CHECKIN)).order_by('-create_time')[:5]

    context = dict(
        user_id=user_profile.user.id,
        user_profile=user_profile,
        group_name=user_profile.groupname,
        title=u'%s管理后台' % user_profile.groupname,
        ongoing_orders=ongoing_orders,
        ongoing_tickets=ongoing_tickets,
    )
    return TemplateResponse(request, 'management/ticket_conductor_dashboard.html', context, current_app='1231')


 # 票据主管 dashboard
def ticket_director_dashboard(request, user_profile):
    # # Get on going orders of transaction
    # ongoing_orders = TransactionOrder.objects.filter(status=TRANSACTION_PROCESSING).order_by('-id')[:10]

    # Get ongoing type of tickets
    pending_tickets = TransactionTicket.objects.filter(
        Q(status=TICKET_RECEIVED_PENDING) |
        Q(status=TICKET_VERIFIED_PENDING) |
        Q(status=TICKET_CHECKIN_PENDING) |
        Q(status=TICKET_CHECKOUT_PENDING)).order_by('-id')[:10]

    context = dict(
        user_id=user_profile.user.id,
        user_profile=user_profile,
        group_name=user_profile.groupname,
        title=u'%s管理后台' % user_profile.groupname,
        # ongoing_orders=ongoing_orders,
        pending_tickets=pending_tickets,
    )
    return TemplateResponse(request, 'management/ticket_director_dashboard.html', context, current_app='1231')


def accountant_dashboard(request, user_profile):
    # Get on going orders of transaction
    ongoing_orders = TransactionOrder.objects.filter(
        status=TRANSACTION_PROCESSING,
        invoice_status=INVOICE_UNLODGED).order_by('-create_time')[:5]

    # Get different type of invoices
    lodged_invoices = Invoice.objects.filter(status=INVOICE_LODGED).order_by('-create_time')[:5]
    finished_invoices = Invoice.objects.filter(status=INVOICE_FINISHED).order_by('-create_time')[:5]

    context = dict(
        user_id=user_profile.user.id,
        user_profile=user_profile,
        group_name=user_profile.groupname,
        title=u'%s管理后台' % user_profile.groupname,
        ongoing_orders=ongoing_orders,
        lodged_invoices=lodged_invoices,
        finished_invoices=finished_invoices,
    )
    return TemplateResponse(request, 'management/accountant_dashboard.html', context, current_app='1231')
