#coding=utf-8
import os
import sys
from collections import deque

from unittest import TestCase
from mock import MagicMock, patch
from django.core.wsgi import get_wsgi_application


os.environ['DJANGO_SETTINGS_MODULE'] = 'TTMS.settings'
application = get_wsgi_application()


from tests.units.utils.test_utils import create_test_request
from management.sites import site as management_site
from management.admin import StaffAdmin


class StaffRegisterTest(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    @patch('django.contrib.auth.models.Group.objects.get')
    @patch('django.contrib.auth.models.User.objects.create_user')
    def test_staff_save_model(self, mock_create_user, mock_group_get):
        model = MagicMock(_meta={})
        obj = MagicMock(email='abc')
        staff_admin_obj = StaffAdmin(model, None)

        request = create_test_request('http://localhost:8000/staff/management/staff/register',
                                      method='post')

        mock_result = MagicMock(is_staff=True, is_active=True, groups=deque())
        mock_create_user.return_value = mock_result
        mock_group_get.return_value = None

        with self.assertRaises(Exception):
            staff_admin_obj.save_model(request, obj, None, False)
