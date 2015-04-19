#coding=utf-8
from unittest import TestCase

from django.contrib.auth.models import User, Group
from mock import MagicMock, patch

from utils.user import get_user_profile


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