#coding=utf-8

from unittest import TestCase

import django
from mock import MagicMock, patch

from ticket.models import TransactionTicket
from transaction.models import TransactionOrder
from member.models import Bank
from ticket.ticket_status import (
    UnreceivedState, ReceivedPendingState, ReceivedState, CheckinPendingState,
    CheckinState, VerifiedPendingState, VerifiedState, CheckoutPendingState,
    CheckoutState)
from utils.constants import (
    InvoiceStatus, INVOICE_STATUS, INVOICE_STATUS2, TicketStatus,
    TICKET_STATUS, TICKET_STATUS2, StaffType)

django.setup()


class TicketTest(TestCase):

    def setUp(self):
        transaction = TransactionOrder()
        self.ticket = TransactionTicket(transaction=transaction,
                                        status=TicketStatus.TICKET_RECEIVED_PENDING)

    def tearDown(self):
        pass

    def test_state_changes(self):
        self.assertEqual(self.ticket.state, None)

        self.ticket.receive_tickets()
        self.assertEqual(type(self.ticket.state), ReceivedPendingState)

        self.ticket.confirm_receive_tickets()
        self.assertEqual(self.ticket.status, TicketStatus.TICKET_RECEIVED)

        self.ticket.checkin_tickets()
        self.assertEqual(self.ticket.status, TicketStatus.TICKET_CHECKIN_PENDING)

        self.ticket.confirm_checkin_tickets()
        self.assertEqual(self.ticket.status, TicketStatus.TICKET_CHECKIN)

        self.ticket.verify_tickets()
        self.assertEqual(self.ticket.status, TicketStatus.TICKET_VERIFIED_PENDING)

        self.ticket.confirm_verify_tickets()
        self.assertEqual(self.ticket.status, TicketStatus.TICKET_VERIFIED)

        self.ticket.checkout_tickets()
        self.assertEqual(self.ticket.status, TicketStatus.TICKET_CHECKOUT_PENDING)

        self.ticket.confirm_checkout_tickets()
        self.assertEqual(self.ticket.status, TicketStatus.TICKET_CHECKOUT)
