#coding=utf-8
from django.shortcuts import get_object_or_404, render_to_response, render, redirect
from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.forms.models import modelformset_factory, inlineformset_factory
from django.forms import ModelForm
from django.views.generic import CreateView, UpdateView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.template import RequestContext
from django.core.exceptions import NON_FIELD_ERRORS
from django.http import HttpResponse, HttpResponseRedirect

from management.models import Staff
from management.auth import login, logout, logout_then_login, redirect_to_login
from transaction.models import (TransactionClaim, TransactionOrder, TRANSACTION_PROCESSING,
    TRANSACTION_DONE, TRANSACTION_ABORT, CLAIM_PENDING, CLAIM_PASSED, CLAIM_ABORT)
from member.models import (Enterprise, Bank, RegisterInvitationCode, MEMBER_ENABLED,
    MEMBER_PENDING, MEMBER_DISABLED, MEMBER_EXPIRED, CODE_ACTIVATED)
from utils.user import get_user_profile
from management.staff_view import BaseStaffView


csrf_protect_m = method_decorator(csrf_protect)


class StaffForm(ModelForm):
    class Meta:
        model = Staff
        fields = '__all__'

        error_messages = {
            NON_FIELD_ERRORS: {
                'unique_together': "%(model_name)s's %(field_labels)s are not unique.",
            }
        }


def main_view(request):
    if not request.user.is_authenticated():
        return redirect_to_login('/management/login')

    user_profile = get_user_profile(request.user)
    staff_view = BaseStaffView.get_staff_view(request, user_profile)

    if staff_view:
        return staff_view.create_dashboard()

    return HttpResponse('error: Unknown Staff Type')
