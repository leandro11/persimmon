#coding=utf-8

import django
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.forms import AuthenticationForm

from utils.user import get_user_profile
from management.models import Staff
from utils.constants import StaffType

# ================================================ LOGIN & AUTH ======================================
from django.contrib.auth import logout as logout_user

def login(request, template_name='management/login.html', redirect_field_name=REDIRECT_FIELD_NAME,
          authentication_form=AuthenticationForm, current_app=None, extra_context=None):
    if request.user.is_authenticated():
        user_profile = get_user_profile(request.user)
        if user_profile.grouptype in StaffType.values:
            return HttpResponseRedirect('/management/main')
        else:
            logout_user(request)

    extra_context = dict(
        title=u'怡智融通贴现后台管理系统',
        site_title=u'怡智融通贴现后台管理系统',
        next='/management/main',
    )
    return django.contrib.auth.views.login(request,
                                           template_name,
                                           redirect_field_name,
                                           authentication_form,
                                           current_app,
                                           extra_context)


def logout(request, next_page=None,
           template_name='management/logged_out.html',
           redirect_field_name=REDIRECT_FIELD_NAME,
           current_app=None, extra_context=None):
    extra_context = dict(site_title=u'怡智融通贴现服务系统')

    return django.contrib.auth.views.logout(request,
                                            next_page,
                                            template_name,
                                            redirect_field_name,
                                            current_app,
                                            extra_context)


def logout_then_login(request, login_url='/management/login/'):
    return django.contrib.auth.views.logout_then_login(request, login_url=login_url)


def redirect_to_login(next, login_url='/management/login/', redirect_field_name=None):
    return django.contrib.auth.views.redirect_to_login(next, login_url, redirect_field_name)
