from unittest import TestCase

from django.contrib.auth.models import User, Group
from mock import MagicMock, patch

from utils.user import get_user_profile


class UserTest(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_get_user_profile(self):
        with self.assertRaises(Exception):
            get_user_profile(1)
