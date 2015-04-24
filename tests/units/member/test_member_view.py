#coding=utf-8

from unittest import TestCase

from mock import MagicMock, patch

from member.member_view import (
    BaseMemberView, BankContactorView, BankOperatorView,
    EnterpriseContactorView, EnterpriseOperatorView)
from utils.constants import MemberUserType


class MemberViewTest(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_get_bank_contactor(self):
        user_profile = MagicMock(grouptype=MemberUserType.BANK_CONTACTOR)
        member_view = BaseMemberView.get_member_view(None, user_profile)

        self.assertEqual(type(member_view), BankContactorView)

    def test_get_bank_operator(self):
        user_profile = MagicMock(grouptype=MemberUserType.BANK_OPERATOR)
        member_view = BaseMemberView.get_member_view(None, user_profile)

        self.assertEqual(type(member_view), BankOperatorView)

    def test_get_enterprise_contactor(self):
        user_profile = MagicMock(grouptype=MemberUserType.ENTERPRISE_CONTACTOR)
        member_view = BaseMemberView.get_member_view(None, user_profile)

        self.assertEqual(type(member_view), EnterpriseContactorView)

    def test_get_enterprise_operator(self):
        user_profile = MagicMock(grouptype=MemberUserType.ENTERPRISE_OPERATOR)
        member_view = BaseMemberView.get_member_view(None, user_profile)

        self.assertEqual(type(member_view), EnterpriseOperatorView)
