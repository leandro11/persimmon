#coding=utf-8
from unittest import TestCase

from mock import MagicMock, patch

from management.staff_view import BaseStaffView, MarketManagerView, TicketConductorView
from utils.constants import StaffType


class StaffViewTest(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_get_market_manager(self):
        user_profile = MagicMock(grouptype=StaffType.MARKET_MANAGER)
        staff_view = BaseStaffView.get_staff_view(None, user_profile)

        self.assertEqual(type(staff_view), MarketManagerView)

    def test_get_ticket_conductor(self):
        user_profile = MagicMock(grouptype=StaffType.TICKET_CONDUCTOR)
        staff_view = BaseStaffView.get_staff_view(None, user_profile)

        self.assertEqual(type(staff_view), TicketConductorView)