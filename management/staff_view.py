#coding=utf-8

from django.template.response import TemplateResponse
from django.db.models import Q

from transaction.models import (TransactionClaim, TransactionOrder, TRANSACTION_PROCESSING,
    TRANSACTION_DONE, TRANSACTION_ABORT)
from member.models import (Enterprise, Bank, RegisterInvitationCode, MEMBER_ENABLED,
    MEMBER_PENDING, MEMBER_DISABLED, MEMBER_EXPIRED, CODE_ACTIVATED)
from utils.constants import StaffType
from ticket.models import TransactionTicket, Invoice
from utils.constants import (
    StaffType, TICKET_RECEIVED_PENDING, TICKET_RECEIVED, TICKET_VERIFIED_PENDING, TICKET_VERIFIED,
    TICKET_CHECKIN_PENDING, TICKET_CHECKIN, TICKET_CHECKOUT_PENDING, TICKET_CHECKOUT,
    INVOICE_LODGED, INVOICE_FINISHED, INVOICE_UNLODGED, TICKET_UNRECEIVED, TransactionClaimStatus)


class BaseStaffView(object):
    """
    Base Staff View
    """

    def __init__(self, request, user_profile):
        """
        :param request: Request object
        :param user_profile: User object
        """
        self.request = request
        self.user_profile = user_profile

    @staticmethod
    def get_staff_view(request, user_profile):
        if user_profile is None:
            return None

        if user_profile.grouptype == StaffType.MARKET_MANAGER:
            return MarketManagerView(request, user_profile)

        if user_profile.grouptype == StaffType.ZONE_MARKET:
            return ZoneMarketView(request, user_profile)

        if user_profile.grouptype == StaffType.SERVICE_MANAGER:
            return ServiceManagerView(request, user_profile)

        if user_profile.grouptype == StaffType.ZONE_SERVICE:
            return ZoneServiceView(request, user_profile)

        if user_profile.grouptype == StaffType.TICKET_DIRECTOR:
            return TicketDirectorView(request, user_profile)

        if user_profile.grouptype == StaffType.TICKET_CONDUCTOR:
            return TicketConductorView(request, user_profile)

        if user_profile.grouptype == StaffType.ACCOUNTANT:
            return AccountantView(request, user_profile)

        if user_profile.grouptype == StaffType.TOP_MANAGER:
            return TopManagerView(request, user_profile)

        return None

    def create_dashboard(self):
        """
        Create staff dashboard
        :return: the dashboard
        """
        raise NotImplementedError()


class MarketManagerView(BaseStaffView):
    """
    Market Manager View
    """
    template_path = 'management/market_dashboard.html'

    def __init__(self, request, user_profile):
        super(MarketManagerView, self).__init__(request, user_profile)

    def create_dashboard(self):
        # Get pending claim for market staff
        pending_claim = TransactionClaim.objects.filter(
            status=TransactionClaimStatus.CLAIM_PENDING).order_by('-create_time')[:5]

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
            user_id=self.user_profile.user.id,
            user_profile=self.user_profile,
            group_name=self.user_profile.groupname,
            title=u'%s管理后台' % self.user_profile.groupname,
            pending_claim=pending_claim,
            enterprise_customers=enterprise_customers,
            bank_customers=bank_customers,
        )
        return TemplateResponse(self.request, self.template_path, context, current_app='1231')


class ZoneMarketView(BaseStaffView):
    """
    Zone Market View
    """
    template_path = 'management/market_dashboard.html'

    def __init__(self, request, user_profile):
        super(ZoneMarketView, self).__init__(request, user_profile)

    def create_dashboard(self):
        # Get pending claim for market staff
        pending_claim = TransactionClaim.objects.filter(
            status=TransactionClaimStatus.CLAIM_PENDING).order_by('-create_time')[:5]

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
            user_id=self.user_profile.user.id,
            user_profile=self.user_profile,
            group_name=self.user_profile.groupname,
            title=u'%s管理后台' % self.user_profile.groupname,
            pending_claim=pending_claim,
            enterprise_customers=enterprise_customers,
            bank_customers=bank_customers,
        )
        return TemplateResponse(self.request, self.template_path, context, current_app='1231')


class ServiceManagerView(BaseStaffView):
    """
    Service Manager View
    """
    template_path = 'management/service_dashboard.html'

    def __init__(self, request, user_profile):
        super(ServiceManagerView, self).__init__(request, user_profile)

    def create_dashboard(self):
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
            user_id=self.user_profile.user.id,
            user_profile=self.user_profile,
            group_name=self.user_profile.groupname,
            title=u'%s管理后台' % self.user_profile.groupname,
            ongoing_orders=ongoing_orders,
            pending_enterprises=pending_enterprises,
            pending_banks=pending_banks,
        )
        return TemplateResponse(self.request, self.template_path, context, current_app='1231')


class ZoneServiceView(BaseStaffView):
    """
    Zone Service View
    """
    template_path = 'management/service_dashboard.html'

    def __init__(self, request, user_profile):
        super(ZoneServiceView, self).__init__(request, user_profile)

    def create_dashboard(self):
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
            user_id=self.user_profile.user.id,
            user_profile=self.user_profile,
            group_name=self.user_profile.groupname,
            title=u'%s管理后台' % self.user_profile.groupname,
            ongoing_orders=ongoing_orders,
            pending_enterprises=pending_enterprises,
            pending_banks=pending_banks,
        )
        return TemplateResponse(self.request, self.template_path, context, current_app='1231')


class TicketDirectorView(BaseStaffView):
    """
    Ticket Director View
    """
    template_path = 'management/ticket_director_dashboard.html'

    def __init__(self, request, user_profile):
        super(TicketDirectorView, self).__init__(request, user_profile)

    def create_dashboard(self):
        # Get on going orders of transaction
        # ongoing_orders = TransactionOrder.objects.filter(status=TRANSACTION_PROCESSING).order_by('-id')[:10]

        # Get ongoing type of tickets
        pending_tickets = TransactionTicket.objects.filter(
            Q(status=TICKET_RECEIVED_PENDING) |
            Q(status=TICKET_VERIFIED_PENDING) |
            Q(status=TICKET_CHECKIN_PENDING) |
            Q(status=TICKET_CHECKOUT_PENDING)).order_by('-id')[:10]

        context = dict(
            user_id=self.user_profile.user.id,
            user_profile=self.user_profile,
            group_name=self.user_profile.groupname,
            title=u'%s管理后台' % self.user_profile.groupname,
            # ongoing_orders=ongoing_orders,
            pending_tickets=pending_tickets,
        )
        return TemplateResponse(self.request, self.template_path, context, current_app='1231')


class TicketConductorView(BaseStaffView):
    """
    Ticket Conductor View
    """
    template_path = 'management/ticket_conductor_dashboard.html'

    def __init__(self, request, user_profile):
        super(TicketConductorView, self).__init__(request, user_profile)

    def create_dashboard(self):
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
            user_id=self.user_profile.user.id,
            user_profile=self.user_profile,
            group_name=self.user_profile.groupname,
            title=u'%s管理后台' % self.user_profile.groupname,
            ongoing_orders=ongoing_orders,
            ongoing_tickets=ongoing_tickets,
        )
        return TemplateResponse(self.request, self.template_path, context, current_app='1231')


class AccountantView(BaseStaffView):
    """
    Accountant View
    """
    template_path = 'management/accountant_dashboard.html'

    def __init__(self, request, user_profile):
        super(AccountantView, self).__init__(request, user_profile)

    def create_dashboard(self):
        # Get on going orders of transaction
        ongoing_orders = TransactionOrder.objects.filter(
            status=TRANSACTION_PROCESSING,
            invoice_status=INVOICE_UNLODGED).order_by('-create_time')[:5]

        # Get different type of invoices
        lodged_invoices = Invoice.objects.filter(status=INVOICE_LODGED).order_by('-create_time')[:5]
        finished_invoices = Invoice.objects.filter(status=INVOICE_FINISHED).order_by('-create_time')[:5]

        context = dict(
            user_id=self.user_profile.user.id,
            user_profile=self.user_profile,
            group_name=self.user_profile.groupname,
            title=u'%s管理后台' % self.user_profile.groupname,
            ongoing_orders=ongoing_orders,
            lodged_invoices=lodged_invoices,
            finished_invoices=finished_invoices,
        )
        return TemplateResponse(self.request, self.template_path, context, current_app='1231')


class TopManagerView(BaseStaffView):
    """
    Top Manager View
    """
    def __init__(self, request, user_profile):
        super(TopManagerView, self).__init__(request, user_profile)

    def create_dashboard(self):
        pass
