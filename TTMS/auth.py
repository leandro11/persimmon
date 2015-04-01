__author__ = 'Lorne'
#coding=utf-8

import django
from utils.user import get_user_profile
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import admin
from utils.constants import *
from management.models import Staff
from django.contrib.auth.decorators import login_required

def member_redirect_to_login(next, login_url='/member/login/', redirect_field_name='next'):
    return django.contrib.auth.views.redirect_to_login(next, login_url, redirect_field_name)


def management_redirect_to_login(next, login_url='/management/login/', redirect_field_name='next'):
    return django.contrib.auth.views.redirect_to_login(next, login_url, redirect_field_name)

@login_required
def login_redirect(request):
    user = request.user

    user.profile = get_user_profile(user)
    if not user.profile:
        # todo report password wrong
        return member_redirect_to_login('/member/login')
    if user.profile.groupname == BANK_CONTACTOR:
        return HttpResponseRedirect('/member/main')
    elif user.profile.groupname == BANK_OPERATOR:
        return HttpResponseRedirect('/member/main')
    elif user.profile.groupname == ENTERPRISE_CONTACTOR:
        return HttpResponseRedirect('/member/main')
    elif user.profile.groupname == ENTERPRISE_OPERATOR:
        return HttpResponseRedirect('/member/main')
    elif isinstance(user.profile, Staff):
        return HttpResponseRedirect('/management/main')
    else:  # todo report password wrong
        return member_redirect_to_login('/member/login')