#coding=utf-8

from django.template.response import TemplateResponse
from django.db.models import Q

from utils.constants import MemberUserType, TransactionClaimStatus
from transaction.models import *

class BaseMemberView(object):
    """
    Base Member View
    """

    def __init__(self, request, user_profile):
        """
        :param request: Request object
        :param user_profile: User object
        """
        self.request = request
        self.user_profile = user_profile

    @staticmethod
    def get_member_view(request, user_profile):
        if user_profile is None:
            return None

        if user_profile.grouptype == MemberUserType.BANK_CONTACTOR:
            return BankContactorView(request, user_profile)

        if user_profile.grouptype == MemberUserType.BANK_OPERATOR:
            return BankOperatorView(request, user_profile)

        if user_profile.grouptype == MemberUserType.ENTERPRISE_CONTACTOR:
            return EnterpriseContactorView(request, user_profile)

        if user_profile.grouptype == MemberUserType.ENTERPRISE_OPERATOR:
            return EnterpriseOperatorView(request, user_profile)

        return None

    def create_dashboard(self):
        """
        Create member dashboard
        :return: the dashboard
        """
        raise NotImplementedError()


class BankContactorView(BaseMemberView):
    """
    Bank Contactor View
    """
    def __init__(self, request, user_profile):
        super(BankContactorView, self).__init__(request, user_profile)

    def create_dashboard(self):
        member = self.user_profile.bank
        is_contactor = True
        contactor_id = member.contactor.id

        ongoing_orders = TransactionOrder.objects.filter(
            Q(status=TRANSACTION_PROCESSING),
            Q(ticket_bank=member.id) | Q(accept_bank=member.id)
        ).order_by('-id')[:10]

        finished_orders = TransactionOrder.objects.filter(
            Q(status=TRANSACTION_DONE),
            Q(ticket_bank=member.id) | Q(accept_bank=member.id)
        ).order_by('-id')[:10]

        pending_claim = TransactionClaim.objects.filter(
            Q(status=TransactionClaimStatus.CLAIM_PENDING),
            Q(ticket_bank=member.id) | Q(accept_bank=member.id)
        ).order_by('-id')[:10]

        for order in ongoing_orders:
            if order.ticket_bank_id == self.user_profile.bank_id:
                order.role = u'贴现银行'
            elif order.accept_bank_id == self.user_profile.bank_id:
                order.role = u'承兑银行'
        for order in finished_orders:
            if order.ticket_bank_id == self.user_profile.bank_id:
                order.role = u'贴现银行'
            elif order.accept_bank_id == self.user_profile.bank_id:
                order.role = u'承兑银行'

        context = dict(
            user_id=self.user_profile.user.id,
            user_profile=self.user_profile,
            member=member,
            title=u'会员首页',
            is_contactor=is_contactor,
            contactor_id=contactor_id,
            ongoing_orders=ongoing_orders,
            finished_orders=finished_orders,
            pending_claim=pending_claim,
        )
        return TemplateResponse(self.request, 'member/main.html', context, current_app='1231')


class BankOperatorView(BaseMemberView):
    """
    Bank Operator View
    """
    def __init__(self, request, user_profile):
        super(BankOperatorView, self).__init__(request, user_profile)

    def create_dashboard(self):
        member = self.user_profile.bank
        is_contactor = False
        contactor_id = member.contactor.id

        ongoing_orders = TransactionOrder.objects.filter(
            Q(status=TRANSACTION_PROCESSING),
            Q(ticket_bank=member.id) | Q(accept_bank=member.id)
        ).order_by('-id')[:10]

        finished_orders = TransactionOrder.objects.filter(
            Q(status=TRANSACTION_DONE),
            Q(ticket_bank=member.id) | Q(accept_bank=member.id)
        ).order_by('-id')[:10]

        pending_claim = TransactionClaim.objects.filter(
            Q(status=TransactionClaimStatus.CLAIM_PENDING),
            Q(ticket_bank=member.id) | Q(accept_bank=member.id)
        ).order_by('-id')[:10]

        for order in ongoing_orders:
            if order.ticket_bank_id == self.user_profile.bank_id:
                order.role = u'贴现银行'
            elif order.accept_bank_id == self.user_profile.bank_id:
                order.role = u'承兑银行'
        for order in finished_orders:
            if order.ticket_bank_id == self.user_profile.bank_id:
                order.role = u'贴现银行'
            elif order.accept_bank_id == self.user_profile.bank_id:
                order.role = u'承兑银行'

        context = dict(
            user_id=self.user_profile.user.id,
            user_profile=self.user_profile,
            member=member,
            title=u'会员首页',
            is_contactor=is_contactor,
            contactor_id=contactor_id,
            ongoing_orders=ongoing_orders,
            finished_orders=finished_orders,
            pending_claim=pending_claim,
        )
        return TemplateResponse(self.request, 'member/main.html', context, current_app='1231')


class EnterpriseContactorView(BaseMemberView):
    """
    Enterprise Contactor View
    """
    def __init__(self, request, user_profile):
        super(EnterpriseContactorView, self).__init__(request, user_profile)

    def create_dashboard(self):
        member = self.user_profile.enterprise
        is_contactor = True
        contactor_id = member.contactor.id

        ongoing_orders = TransactionOrder.objects.filter(
            Q(status=TRANSACTION_PROCESSING),
            Q(receivable_enterprise=member.id) | Q(pay_enterprise=member.id)
        ).order_by('-id')[:10]

        finished_orders = TransactionOrder.objects.filter(
            Q(status=TRANSACTION_DONE),
            Q(receivable_enterprise=member.id) | Q(pay_enterprise=member.id)
        ).order_by('-id')[:10]

        pending_claim = TransactionClaim.objects.filter(
            Q(status=TransactionClaimStatus.CLAIM_PENDING),
            Q(receivable_enterprise=member.id) | Q(pay_enterprise=member.id)
        ).order_by('-id')[:10]

        for order in ongoing_orders:
            if order.receivable_enterprise_id == self.user_profile.enterprise_id:
                order.role = u'收款方'
            elif order.pay_enterprise_id == self.user_profile.enterprise_id:
                order.role = u'付款方'

        for order in finished_orders:
            if order.receivable_enterprise_id == self.user_profile.enterprise_id:
                order.role = u'收款方'
            elif order.pay_enterprise_id == self.user_profile.enterprise_id:
                order.role = u'付款方'

        context = dict(
            user_id=self.user_profile.user.id,
            user_profile=self.user_profile,
            member=member,
            title=u'会员首页',
            is_contactor=is_contactor,
            contactor_id=contactor_id,
            ongoing_orders=ongoing_orders,
            finished_orders=finished_orders,
            pending_claim=pending_claim,
        )
        return TemplateResponse(self.request, 'member/main.html', context, current_app='1231')


class EnterpriseOperatorView(BaseMemberView):
    """
    Enterprise Operator View
    """
    def __init__(self, request, user_profile):
        super(EnterpriseOperatorView, self).__init__(request, user_profile)

    def create_dashboard(self):
        member = self.user_profile.enterprise
        is_contactor = False
        contactor_id = member.contactor.id

        ongoing_orders = TransactionOrder.objects.filter(
            Q(status=TRANSACTION_PROCESSING),
            Q(receivable_enterprise=member.id) | Q(pay_enterprise=member.id)
        ).order_by('-id')[:10]

        finished_orders = TransactionOrder.objects.filter(
            Q(status=TRANSACTION_DONE),
            Q(receivable_enterprise=member.id) | Q(pay_enterprise=member.id)
        ).order_by('-id')[:10]

        pending_claim = TransactionClaim.objects.filter(
            Q(status=TransactionClaimStatus.CLAIM_PENDING),
            Q(receivable_enterprise=member.id) | Q(pay_enterprise=member.id)
        ).order_by('-id')[:10]

        for order in ongoing_orders:
            if order.receivable_enterprise_id == self.user_profile.enterprise_id:
                order.role = u'收款方'
            elif order.pay_enterprise_id == self.user_profile.enterprise_id:
                order.role = u'付款方'

        for order in finished_orders:
            if order.receivable_enterprise_id == self.user_profile.enterprise_id:
                order.role = u'收款方'
            elif order.pay_enterprise_id == self.user_profile.enterprise_id:
                order.role = u'付款方'

        context = dict(
            user_id=self.user_profile.user.id,
            user_profile=self.user_profile,
            member=member,
            title=u'会员首页',
            is_contactor=is_contactor,
            contactor_id=contactor_id,
            ongoing_orders=ongoing_orders,
            finished_orders=finished_orders,
            pending_claim=pending_claim,
        )
        return TemplateResponse(self.request, 'member/main.html', context, current_app='1231')

