#coding=utf-8

import django
from django.shortcuts import render
from django.shortcuts import get_object_or_404, render_to_response, render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template.response import TemplateResponse
from django.forms.models import modelformset_factory, inlineformset_factory
from django.forms import ModelForm
from django.views.generic import CreateView, UpdateView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.template import RequestContext
from django.contrib.auth.models import User, Group, AnonymousUser
from django.db.models import Q
from django.contrib.auth import logout
from django.http import Http404, HttpResponseRedirect
from django.core.exceptions import PermissionDenied
from django.utils.http import urlquote, urlunquote

from transaction.models import *
from utils.func import *
from utils.user import get_user_profile
from member.models import *
from member.auth import login, logout, logout_then_login, redirect_to_login  #password_reset, password_change,
from member.member_view import BaseMemberView


csrf_protect_m = method_decorator(csrf_protect)


class BankForm(ModelForm):
    class Meta:
        model = Bank
        fields = '__all__'


class BankCreateView(CreateView):
    model = Bank
    template_name = 'member/bank_register2.html'


def bank_register(request):
    BankSet = modelformset_factory(Bank, exclude=('expired_date',))
    ContactorSet = inlineformset_factory(Bank, BankContactor, can_delete=False, max_num=1, exclude=('user', 'bank'))
    OperatorSet = inlineformset_factory(Bank, BankOperator, extra=1, can_delete=False, max_num=1, exclude=('user', 'bank'))
    # ContactorSet =modelformset_factory(BankContactor, exclude=('expired_date',))
    # OperatorSet = modelformset_factory(BankOperator, exclude=('expired_date',))
    operator_formset = OperatorSet()
    contact_formset = ContactorSet()

    if not request.method == 'POST':
        bank_formset = BankForm()
    else:
        # contact_formset = ContactorSet(request.POST or None, request.FILES)
        # operator_formset = OperatorSet(request.POST or None, request.FILES)
        bank_formset = BankForm(request.POST or None, request.FILES)

        if bank_formset.is_valid():
            # bank_formset.save()
            return HttpResponse('123123')
            # if contact_formset.is_valid():
            #     # contact_formset.save()
            #     return HttpResponse('123123')
            # if operator_formset.is_valid():
            #     # operator_formset.save()
            #     return HttpResponse('123123')

    return render_to_response("member/bank_register.html", {
        "bank_formset": bank_formset,
        'contact_formset': contact_formset,
        'operator_formset': operator_formset,
        "title": u'银行会员注册',
    }, context_instance=RequestContext(request))


def create_bank(request):
    #create new
    if request.method == 'POST':
        BankSet = modelformset_factory(Bank, exclude=('expired_date',))
        bank_formset = BankSet(request.POST or None, request.FILES)
        ContactorSet = inlineformset_factory(Bank, BankContactor, can_delete=False, max_num=1, exclude=('user', 'bank'))
        OperatorSet = inlineformset_factory(Bank, BankOperator, extra=1, can_delete=False, max_num=1, exclude=('user', 'bank'))

        contact_formset = ContactorSet(request.POST or None, request.FILES)
        operator_formset = OperatorSet(request.POST or None, request.FILES)

        if bank_formset.is_valid():
            bank_formset.save()
        else:
            return render_to_response("member/bank_register.html", {
                "bank_formset": bank_formset,
                'contact_formset': contact_formset,
                'operator_formset': operator_formset,
                "title": u'银行会员注册',
            },
                                      context_instance=RequestContext(request)
            )
    return HttpResponse('123123')


def bank_login(request):
    return HttpResponse('123123')


def enterprise_register(request):
    EnterpriseSet = modelformset_factory(Enterprise)
    formset = EnterpriseSet()
    return render_to_response("member/enterprise_register.html", {
        "formset": formset,
        "title": u'企业会员注册',
    })


def enterprise_login(request):
    return HttpResponse('123123')


def member_main(request):
    user = request.user
    if not user.is_authenticated():
        return redirect_to_login('/member/login')

    user_profile = get_user_profile(user)
    member_view = BaseMemberView.get_member_view(request, user_profile)

    if member_view:
        return member_view.create_dashboard()

    # Only enterprise member or bank member could login
    logout(request)
    return HttpResponseRedirect('/member/login')


def get_bank_attachment(request, bank_id, filename):
    if not request.user.is_authenticated():
        raise PermissionDenied
    if filename:
        # name = urlunquote(filename)
        attachment = BankAttachment.objects.get(name=filename)
        filename = attachment.file.path
        return show_file(filename)

    return Http404

def get_bank_attachment_thumbnail(request, bank_id, filename):
    if not request.user.is_authenticated():
        raise PermissionDenied
    if filename:
        # name = urlunquote(filename)
        attachment = BankAttachment.objects.get(name=filename)
        filename = attachment.thumbnail.path
        return show_file(filename)

    return Http404

def get_enterprise_attachment(request, enterprise_id, filename):
    if not request.user.is_authenticated():
        raise PermissionDenied
    if filename:
        # name = urlunquote(filename)
        attachment = EnterpriseAttachment.objects.get(name=filename)
        filename = attachment.file.path
        return show_file(filename)

def get_enterprise_attachment_thumbnail(request, enterprise_id, filename):
    if not request.user.is_authenticated():
        raise PermissionDenied
    if filename:
        # name = urlunquote(filename)
        attachment = EnterpriseAttachment.objects.get(name=filename)
        filename = attachment.thumbnail.path
        return show_file(filename)

    return Http404