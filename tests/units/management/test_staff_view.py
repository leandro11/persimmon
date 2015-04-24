#coding=utf-8

from unittest import TestCase

from mock import MagicMock, patch

from management.staff_view import (
    BaseStaffView, MarketManagerView, ZoneMarketView, ServiceManagerView,
    ZoneServiceView, TicketDirectorView, AccountantView, TopManagerView, TicketConductorView)
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


    def test_get_zone_market(self):
        user_profile = MagicMock(grouptype=StaffType.ZONE_MARKET)
        staff_view = BaseStaffView.get_staff_view(None, user_profile)

        self.assertEqual(type(staff_view), ZoneMarketView)


    def test_get_service_manager(self):
        user_profile = MagicMock(grouptype=StaffType.SERVICE_MANAGER)
        staff_view = BaseStaffView.get_staff_view(None, user_profile)

        self.assertEqual(type(staff_view), ServiceManagerView)


    def test_get_zone_service(self):
        user_profile = MagicMock(grouptype=StaffType.ZONE_SERVICE)
        staff_view = BaseStaffView.get_staff_view(None, user_profile)

        self.assertEqual(type(staff_view), ZoneServiceView)


    def test_get_ticket_director(self):
        user_profile = MagicMock(grouptype=StaffType.TICKET_DIRECTOR)
        staff_view = BaseStaffView.get_staff_view(None, user_profile)

        self.assertEqual(type(staff_view), TicketDirectorView)


    def test_get_ticket_conductor(self):
        user_profile = MagicMock(grouptype=StaffType.TICKET_CONDUCTOR)
        staff_view = BaseStaffView.get_staff_view(None, user_profile)

        self.assertEqual(type(staff_view), TicketConductorView)


    def test_get_accountant(self):
        user_profile = MagicMock(grouptype=StaffType.ACCOUNTANT)
        staff_view = BaseStaffView.get_staff_view(None, user_profile)

        self.assertEqual(type(staff_view), AccountantView)


    def test_get_top_manager(self):
        user_profile = MagicMock(grouptype=StaffType.TOP_MANAGER)
        staff_view = BaseStaffView.get_staff_view(None, user_profile)

        self.assertEqual(type(staff_view), TopManagerView)
