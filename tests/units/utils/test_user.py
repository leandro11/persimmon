#coding=utf-8
from unittest import TestCase

from django.contrib.auth.models import User, Group
from mock import MagicMock, patch

from utils.user import get_user_profile, is_staff_user, is_member_user


class UserTest(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    @patch('management.models.Staff.objects.get')
    @patch('django.contrib.auth.models.User.objects.get')
    def test_get_user_profile(self, mock_get, mock_staff_get):
        groups = MagicMock(all=lambda: [Group(id=5, name=u'市场部总经理')])
        mock_get.return_value = MagicMock(groups=groups)

        get_user_profile(1)
        self.assertEqual(mock_staff_get.call_count, 1)

    @patch('management.models.Staff.objects.get')
    @patch('django.contrib.auth.models.User.objects.get')
    def test_is_staff_user(self, mock_get, mock_staff_get):
        groups = MagicMock(all=lambda: [Group(id=5, name=u'市场部总经理')])
        mock_get.return_value = MagicMock(groups=groups)

        self.assertTrue(is_staff_user(1))

    @patch('member.models.EnterpriseOperator.objects.get')
    @patch('django.contrib.auth.models.User.objects.get')
    def test_is_member_user(self, mock_get, mock_staff_get):
        groups = MagicMock(all=lambda: [Group(id=2, name=u'银行会员执行人')])
        mock_get.return_value = MagicMock(groups=groups)

        self.assertTrue(is_member_user(1))
