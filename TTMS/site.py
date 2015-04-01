#coding=utf-8
from django.contrib import admin
from django.conf import settings
from functools import update_wrapper
from django.utils import six
from django.core.exceptions import PermissionDenied, ValidationError
from member import auth
from member.views import member_main
import django
from utils.user import group_check, get_group, get_user_profile
from utils.constants import *
from django.views.decorators.cache import never_cache
from django.contrib.admin.forms import AdminAuthenticationForm
from django.contrib.auth import logout as logout_user
from django.http import HttpResponse, HttpResponseRedirect


class SuperAdminSite(admin.AdminSite):
    def app_index(self, request, app_label, extra_context=None):
        if request.user.is_superuser:
            return super(SuperAdminSite, self).app_index(request, app_label, extra_context)
        else:
            logout_user(request)
            return HttpResponseRedirect('/admin/login')


    # def has_permission(self, request):
    #     if request.user.is_superuser:
    #         return super(SuperAdminSite, self).has_permission(request)
    #     else:
    #         logout_user(request)
    #         return HttpResponseRedirect('/admin/login')

    def index(self, request, extra_context=None):
        if request.user.is_superuser:
            return super(SuperAdminSite, self).index(request, extra_context)
        else:
            logout_user(request)
            return HttpResponseRedirect('/admin/login')


site = SuperAdminSite()