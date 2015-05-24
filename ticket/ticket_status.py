#coding=utf-8

from utils.constants import TicketStatus, StaffType


class TicketState(object):
    """
    Basic Ticket State
    """

    def __init__(self, ticket_obj):
        """
        :param request: TransactionTicket Object
        """
        self.ticket_obj = ticket_obj

    def receive_tickets(self, **kwargs):
        raise NotImplementedError()

    def confirm_receive_tickets(self, **kwargs):
        raise NotImplementedError()

    def verify_tickets(self, **kwargs):
        raise NotImplementedError()

    def confirm_verify_tickets(self, **kwargs):
        raise NotImplementedError()

    def checkin_tickets(self, **kwargs):
        raise NotImplementedError()

    def confirm_checkin_tickets(self, **kwargs):
        raise NotImplementedError()

    def checkout_tickets(self, **kwargs):
        raise NotImplementedError()

    def confirm_checkout_tickets(self, **kwargs):
        raise NotImplementedError()

    def show_link(self, **kwargs):
        raise NotImplementedError()


class UnreceivedState(TicketState):

    def __init__(self, ticket_obj):
        super(UnreceivedState, self).__init__(ticket_obj)

    def receive_tickets(self, **kwargs):
        # Change current ticket_obj's status
        self.ticket_obj.status = TicketStatus.TICKET_RECEIVED_PENDING

    def confirm_receive_tickets(self, **kwargs):
        pass

    def verify_tickets(self, **kwargs):
        pass

    def confirm_verify_tickets(self, **kwargs):
        pass

    def checkin_tickets(self, **kwargs):
        pass

    def confirm_checkin_tickets(self, **kwargs):
        pass

    def checkout_tickets(self, **kwargs):
        pass

    def confirm_checkout_tickets(self, **kwargs):
        pass

    def show_link(self, **kwargs):
        """
        :return: order of link for next step, as 'receive, checkin, verify, checkout'
        """
        return [u'', u'', u'', u'']


class ReceivedPendingState(TicketState):

    def __init__(self, ticket_obj):
        super(ReceivedPendingState, self).__init__(ticket_obj)

    def receive_tickets(self, **kwargs):
        pass

    def confirm_receive_tickets(self, **kwargs):
        # Change current ticket_obj's status
        self.ticket_obj.status = TicketStatus.TICKET_RECEIVED

    def verify_tickets(self, **kwargs):
        pass

    def confirm_verify_tickets(self, **kwargs):
        pass

    def checkin_tickets(self, **kwargs):
        pass

    def confirm_checkin_tickets(self, **kwargs):
        pass

    def checkout_tickets(self, **kwargs):
        pass

    def confirm_checkout_tickets(self, **kwargs):
        pass

    def show_link(self, **kwargs):
        if kwargs.get('role') == StaffType.TICKET_DIRECTOR:
            return [
                u'<a class="button" href="/staff/ticket/transactionticket/?receive_confirm=%s"><strong>确认收票</strong></a>' % self.ticket_obj.id,
                u'',
                u'',
                u''
            ]

        return [
            u'收票待核',
            u'',
            u'',
            u''
        ]


class ReceivedState(TicketState):

    def __init__(self, ticket_obj):
        super(ReceivedState, self).__init__(ticket_obj)

    def receive_tickets(self, **kwargs):
        pass

    def confirm_receive_tickets(self, **kwargs):
        pass

    def verify_tickets(self, **kwargs):
        pass

    def confirm_verify_tickets(self, **kwargs):
        pass

    def checkin_tickets(self, **kwargs):
        # Change current ticket_obj's status
        self.ticket_obj.status = TicketStatus.TICKET_CHECKIN_PENDING

    def confirm_checkin_tickets(self, **kwargs):
        pass

    def checkout_tickets(self, **kwargs):
        pass

    def confirm_checkout_tickets(self, **kwargs):
        pass

    def show_link(self, **kwargs):
        if kwargs.get('role') == StaffType.TICKET_DIRECTOR:
            return [
                u'收票完成',
                u'等待入库',
                u'',
                u''
            ]

        return [
            u'收票完成',
            u'<a class="button" href="/staff/ticket/transactionticket/%s/checkin"><strong>执行入库</strong></a>' % self.ticket_obj.id,
            u'',
            u''
        ]


class CheckinPendingState(TicketState):

    def __init__(self, ticket_obj):
        super(CheckinPendingState, self).__init__(ticket_obj)

    def receive_tickets(self, **kwargs):
        pass

    def confirm_receive_tickets(self, **kwargs):
        pass

    def verify_tickets(self, **kwargs):
        pass

    def confirm_verify_tickets(self, **kwargs):
        pass

    def checkin_tickets(self, **kwargs):
        pass

    def confirm_checkin_tickets(self, **kwargs):
        # Change current ticket_obj's status
        self.ticket_obj.status = TicketStatus.TICKET_CHECKIN

    def checkout_tickets(self, **kwargs):
        pass

    def confirm_checkout_tickets(self, **kwargs):
        pass

    def show_link(self, **kwargs):
        if kwargs.get('role') == StaffType.TICKET_DIRECTOR:
            return [
                u'收票完成',
                u'<a class="button" href="/staff/ticket/transactionticket/?checkin_confirm=%s"><strong>确认入库</strong></a>' % self.ticket_obj.id,
                u'',
                u''
            ]

        return [
            u'收票完成',
            u'等待审核',
            u'',
            u''
        ]


class CheckinState(TicketState):

    def __init__(self, ticket_obj):
        super(CheckinState, self).__init__(ticket_obj)

    def receive_tickets(self, **kwargs):
        pass

    def confirm_receive_tickets(self, **kwargs):
        pass

    def verify_tickets(self, **kwargs):
        # Change current ticket_obj's status
        self.ticket_obj.status = TicketStatus.TICKET_VERIFIED_PENDING

    def confirm_verify_tickets(self, **kwargs):
        pass

    def checkin_tickets(self, **kwargs):
        pass

    def confirm_checkin_tickets(self, **kwargs):
        pass

    def checkout_tickets(self, **kwargs):
        pass

    def confirm_checkout_tickets(self, **kwargs):
        pass

    def show_link(self, **kwargs):
        if kwargs.get('role') == StaffType.TICKET_DIRECTOR:
            return [
                u'收票完成',
                u'入库完成',
                u'等待验票',
                u''
            ]

        return [
            u'收票完成',
            u'入库完成',
            u'<a class="button" href="/staff/ticket/transactionticket/?verify_pending=%s"><strong>执行验票</strong></a>' % self.ticket_obj.id,
            u''
        ]


class VerifiedPendingState(TicketState):

    def __init__(self, ticket_obj):
        super(VerifiedPendingState, self).__init__(ticket_obj)

    def receive_tickets(self, **kwargs):
        pass

    def confirm_receive_tickets(self, **kwargs):
        pass

    def verify_tickets(self, **kwargs):
        pass

    def confirm_verify_tickets(self, **kwargs):
        # Change current ticket_obj's status
        self.ticket_obj.status = TicketStatus.TICKET_VERIFIED

    def checkin_tickets(self, **kwargs):
        pass

    def confirm_checkin_tickets(self, **kwargs):
        pass

    def checkout_tickets(self, **kwargs):
        pass

    def confirm_checkout_tickets(self, **kwargs):
        pass

    def show_link(self, **kwargs):
        if kwargs.get('role') == StaffType.TICKET_DIRECTOR:
            return [
                u'收票完成',
                u'入库完成',
                u'<a class="button" href="/staff/ticket/transactionticket/?verify_confirm=%s"><strong>确认验票</strong></a>' % self.ticket_obj.id,
                u''
            ]

        return [
            u'收票完成',
            u'入库完成',
            u'等待审核',
            u''
        ]


class VerifiedState(TicketState):

    def __init__(self, ticket_obj):
        super(VerifiedState, self).__init__(ticket_obj)

    def receive_tickets(self, **kwargs):
        pass

    def confirm_receive_tickets(self, **kwargs):
        pass

    def verify_tickets(self, **kwargs):
        pass

    def confirm_verify_tickets(self, **kwargs):
        pass

    def checkin_tickets(self, **kwargs):
        pass

    def confirm_checkin_tickets(self, **kwargs):
        pass

    def checkout_tickets(self, **kwargs):
        # Change current ticket_obj's status
        self.ticket_obj.status = TicketStatus.TICKET_CHECKOUT_PENDING

    def confirm_checkout_tickets(self, **kwargs):
        pass

    def show_link(self, **kwargs):
        if kwargs.get('role') == StaffType.TICKET_DIRECTOR:
            return [
                u'收票完成',
                u'入库完成',
                u'验票完成',
                u'等待出库'
            ]

        return [
            u'收票完成',
            u'入库完成',
            u'验票完成',
            u'<a class="button" href="/staff/ticket/transactionticket/?checkout_pending=%s"><strong>执行出库</strong></a>' % self.ticket_obj.id
        ]


class CheckoutPendingState(TicketState):

    def __init__(self, ticket_obj):
        super(CheckoutPendingState, self).__init__(ticket_obj)

    def receive_tickets(self, **kwargs):
        pass

    def confirm_receive_tickets(self, **kwargs):
        pass

    def verify_tickets(self, **kwargs):
        pass

    def confirm_verify_tickets(self, **kwargs):
        pass

    def checkin_tickets(self, **kwargs):
        pass

    def confirm_checkin_tickets(self, **kwargs):
        pass

    def checkout_tickets(self, **kwargs):
        pass

    def confirm_checkout_tickets(self, **kwargs):
        # Change current ticket_obj's status
        self.ticket_obj.status = TicketStatus.TICKET_CHECKOUT

    def show_link(self, **kwargs):
        if kwargs.get('role') == StaffType.TICKET_DIRECTOR:
            return [
                u'收票完成',
                u'入库完成',
                u'验票完成',
                u'<a class="button" href="/staff/ticket/transactionticket/?checkout_confirm=%s"><strong>确认出库</strong></a>' % self.ticket_obj.id
            ]

        return [
            u'收票完成',
            u'入库完成',
            u'验票完成',
            u'等待审核'
        ]


class CheckoutState(TicketState):

    def __init__(self, ticket_obj):
        super(CheckoutState, self).__init__(ticket_obj)

    def receive_tickets(self, **kwargs):
        pass

    def confirm_receive_tickets(self, **kwargs):
        pass

    def verify_tickets(self, **kwargs):
        pass

    def confirm_verify_tickets(self, **kwargs):
        pass

    def checkin_tickets(self, **kwargs):
        pass

    def confirm_checkin_tickets(self, **kwargs):
        pass

    def checkout_tickets(self, **kwargs):
        pass

    def confirm_checkout_tickets(self, **kwargs):
        pass

    def show_link(self, **kwargs):
        if kwargs.get('role') == StaffType.TICKET_DIRECTOR:
            return [
                u'收票完成',
                u'入库完成',
                u'验票完成',
                u'出库完成'
            ]

        return [
            u'收票完成',
            u'入库完成',
            u'验票完成',
            u'出库完成'
        ]

