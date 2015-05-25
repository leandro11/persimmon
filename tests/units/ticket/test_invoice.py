#coding=utf-8

from unittest import TestCase

import django
from mock import MagicMock, patch

from ticket.models import Invoice
from transaction.models import TransactionOrder
from ticket.invoice_status import (
    UnlodgedState, LodgedState, FinishedState, AbortState)
from utils.constants import (
    InvoiceStatus, INVOICE_STATUS, INVOICE_STATUS2, TicketStatus,
    TICKET_STATUS, TICKET_STATUS2, StaffType)

django.setup()


class InvoiceTest(TestCase):

    def setUp(self):
        transaction = TransactionOrder()
        self.invoice = Invoice(transaction=transaction,
                               status=InvoiceStatus.INVOICE_LODGED)

    def tearDown(self):
        pass

    def test_state_changes(self):
        self.assertEqual(self.invoice.state, None)

        self.invoice.show_link()
        self.assertEqual(type(self.invoice.state), LodgedState)

        self.invoice.send()
        self.assertEqual(self.invoice.status, InvoiceStatus.INVOICE_FINISHED)
