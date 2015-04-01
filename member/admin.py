#coding=utf-8

from django.contrib import admin
from member.models import *
from django.http import HttpResponse
from django.conf.urls import patterns
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from django.db import transaction
from django.forms.formsets import all_valid
from django.contrib.admin import widgets, helpers
from django.utils.encoding import force_text, python_2_unicode_compatible
from django.utils.translation import ugettext as _
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_permission_codename
from django.core.exceptions import (PermissionDenied, ValidationError, FieldError, ImproperlyConfigured)
from django.contrib.admin.utils import (quote, unquote, flatten_fieldsets,
                                        get_deleted_objects, model_format_dict, NestedObjects,
                                        lookup_needs_distinct)
from django.forms.models import (modelform_factory, modelformset_factory,
                                 inlineformset_factory, BaseInlineFormSet, modelform_defines_fields)
from django.utils.crypto import get_random_string
import random, datetime
import sys
from django.forms import ModelForm
from django import forms
from django.core import validators
from django.contrib.auth.models import User, Group
from utils.constants import BANK_CONTACTOR, BANK_OPERATOR, ENTERPRISE_CONTACTOR, ENTERPRISE_OPERATOR, MEMBER_USER_TYPE, MARKET_MANAGER, ZONE_MARKET, TOP_MANAGER, SERVICE_MANAGER, \
    ZONE_SERVICE
from utils.user import group_check, get_group, get_user_profile
from member.form import *
from django.http import Http404, HttpResponseRedirect
from django.contrib.admin.exceptions import DisallowedModelAdminToField
from django.utils.html import escape, escapejs
from django.core.urlresolvers import reverse
from member.sites import site as member_site
from management.sites import site as management_site
from django.shortcuts import get_object_or_404, render_to_response
from django.contrib import messages
from django.contrib.messages.storage.fallback import FallbackStorage

reload(sys)
sys.setdefaultencoding('utf-8')

csrf_protect_m = method_decorator(csrf_protect)
IS_POPUP_VAR = '_popup'
TO_FIELD_VAR = '_to_field'


class RegisterInvitationCodeAdmin(admin.ModelAdmin):
    list_display = ('member_name', 'member_type', 'code', 'status', 'market_manager', 'create_date')
    search_fields = ('member_name', 'member_type', 'status')
    # list_editable = ('member_type', 'status',)
    # list_filter = ('member_type', 'status',)
    readonly_fields = []

    def get_urls(self):
        urls = super(RegisterInvitationCodeAdmin, self).get_urls()
        my_urls = patterns('',
                           (r'^(.+)/confirm/$', self.confirm_view),  # 审核会员推荐
        )
        return my_urls + urls

    def generate_code(self, length=20, allowed_chars='ABCDEFGHJKLMNPQRSTUVWXYZ0123456789'):
        """
        from django.utils.crypto import get_random_string
        """
        return get_random_string(length, allowed_chars)

    def add_view(self, request, form_url='', extra_context=None):
        self.exclude = ['code', 'market_manager', 'status', 'used_date', 'create_date', 'referee_member_type', 'referee_member_id']
        self.readonly_fields = []
        self.form = ModelForm

        user_profile = get_user_profile(request.user)
        group_name = None if user_profile is None else user_profile.groupname

        if request.user.is_superuser:
            return super(RegisterInvitationCodeAdmin, self).add_view(request, form_url, extra_context)
        elif group_name in (MARKET_MANAGER, ZONE_MARKET, TOP_MANAGER):
            self.add_form_template = 'management/change_form.html'
        elif group_name in (BANK_OPERATOR, BANK_CONTACTOR, ENTERPRISE_CONTACTOR, ENTERPRISE_OPERATOR):
            # todo modify invite code add form for contactor
            self.add_form_template = 'member/member_change_form.html'
            extra_context = dict(title=u'推荐新会员注册', )
        else:
            raise PermissionDenied

        return super(RegisterInvitationCodeAdmin, self).add_view(request, form_url, extra_context)

    def save_model(self, request, obj, form, change):
        #for add_view
        if request.path.find('/add') > 0:
            user_profile = get_user_profile(request.user)
            group_name = None if user_profile is None else user_profile.groupname

            #若是企业用户添加，则自动填补referee_member_type和referee_member_id字段
            if group_name == BANK_OPERATOR or group_name == BANK_CONTACTOR:
                obj.referee_member_type = BANK_MEMBER
                obj.referee_member_id = user_profile.bank.id
                obj.market_manager = user_profile.bank.referee_manager
                obj.status = CODE_PENDING
            elif group_name == ENTERPRISE_CONTACTOR or group_name == ENTERPRISE_OPERATOR:
                obj.referee_member_type = ENTERPRISE_MEMBER
                obj.referee_member_id = user_profile.enterprise.id
                obj.market_manager = user_profile.enterprise.referee_manager
                obj.status = CODE_PENDING
            # 工作人员推荐
            else:
                staffs = Staff.objects.filter(user=request.user)
                if staffs.count() > 0:
                    obj.market_manager = staffs[0]

            if not obj.code:
                code = self.generate_code()
                #check whether unique
                while (RegisterInvitationCode.objects.filter(code=code).count() > 0):
                    code = self.generate_code()
                obj.code = code
        #for confirm_view
        elif request.path.find('/confirm') > 0:
            obj.status = CODE_ACTIVATED

        obj.save()


    def change_view(self, request, object_id, form_url='', extra_context=None):
        self.exclude = ['referee_member_type', 'referee_member_id']
        self.readonly_fields = ['code', 'market_manager', 'create_date']

        user_profile = get_user_profile(request.user)
        group_name = None if user_profile is None else user_profile.groupname
        obj = RegisterInvitationCode.objects.get(id=long(object_id))

        if request.user.is_superuser:
            self.exclude = []
        elif group_name in (MARKET_MANAGER, ZONE_MARKET, TOP_MANAGER):
            self.change_form_template = 'management/change_form.html'
        elif group_name in (BANK_OPERATOR, BANK_CONTACTOR, ENTERPRISE_CONTACTOR, ENTERPRISE_OPERATOR):
            if group_name in (BANK_OPERATOR, BANK_CONTACTOR):
                if not obj.referee_member_type == BANK_MEMBER or not obj.referee_member_id == user_profile.bank.id:
                    return Http404
            elif group_name in (ENTERPRISE_CONTACTOR, ENTERPRISE_OPERATOR):
                if not obj.referee_member_type == ENTERPRISE_MEMBER or not obj.referee_member_id == user_profile.enterprise.id:
                    return Http404

            self.readonly_fields = ['member_name', 'member_type', 'contactor_name', 'contactor_email', 'status', 'code', 'market_manager', 'create_date']
            # todo template的导航栏增加推荐新会员列表
            self.change_form_template = 'member/member_change_form.html'
        else:
            return Http404

        if obj.status == CODE_USED:
            self.readonly_fields += ['used_date']
        else:
            self.exclude += ['used_date']

        if obj.referee_member_type and obj.referee_member_id:
            self.form = RegisterInviteCodeChangeForm
        else:
            self.form = RegisterInviteCodeShowForm
            # self.readonly_fields += ['referee_member']

        return super(RegisterInvitationCodeAdmin, self).change_view(request, object_id, form_url, extra_context)

    def changelist_view(self, request, extra_context=None):
        self.list_filter = ('member_type', 'status',)
        if request.user.is_superuser:
            return super(RegisterInvitationCodeAdmin, self).changelist_view(request, extra_context)

        user_profile = get_user_profile(request.user)
        group_name = None if user_profile is None else user_profile.groupname
        if group_name in (MARKET_MANAGER, ZONE_MARKET, TOP_MANAGER):
            self.change_list_template = 'management/change_list.html'
        elif group_name in (BANK_OPERATOR, BANK_CONTACTOR, ENTERPRISE_CONTACTOR, ENTERPRISE_OPERATOR):
            self.change_list_template = 'member/change_list.html'
            self.list_filter = ()
        extra_context = dict(title=u'会员推荐记录', )
        return super(RegisterInvitationCodeAdmin, self).changelist_view(request, extra_context)

    @transaction.atomic
    def confirm_view(self, request, object_id, form_url='', extra_context=None):
        self.exclude = ['referee_member_type', 'referee_member_id']
        self.readonly_fields = ['status', 'code', 'market_manager', 'create_date']
        user_profile = get_user_profile(request.user)
        group_name = None if user_profile is None else user_profile.groupname

        obj = RegisterInvitationCode.objects.get(id=long(object_id))
        if obj.status == CODE_USED:
            self.readonly_fields += ['used_date']
        else:
            self.exclude += ['used_date']
        if obj.referee_member_type and obj.referee_member_id:
            self.form = RegisterInviteCodeChangeForm
        else:
            self.form = RegisterInviteCodeShowForm

        if request.user.is_superuser:
            pass
            #return super(RegisterInvitationCodeAdmin, self).change_view(request, object_id, form_url, extra_context)
        elif group_name in (MARKET_MANAGER, ZONE_MARKET, TOP_MANAGER):
            self.change_form_template = 'management/change_form.html'
        else:
            return Http404
        extra_context = dict(title=u'审核会员推荐', )
        return super(RegisterInvitationCodeAdmin, self).change_view(request, object_id, form_url, extra_context)

    def get_queryset(self, request):
        qs = super(RegisterInvitationCodeAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        user_profile = get_user_profile(request.user)
        group_name = None if user_profile is None else user_profile.groupname

        # 限制只能看见自己单位的邀请记录
        if group_name in (MARKET_MANAGER, ZONE_MARKET):
            return qs.filter(market_manager_id=user_profile.id)
        elif group_name in (BANK_CONTACTOR, BANK_OPERATOR):
            return qs.filter(referee_member_type=BANK_MEMBER, referee_member_id=user_profile.bank_id)
        elif group_name in (ENTERPRISE_CONTACTOR, ENTERPRISE_OPERATOR):
            return qs.filter(referee_member_type=ENTERPRISE_MEMBER, referee_member_id=user_profile.enterprise_id)
        elif group_name == TOP_MANAGER:
            return qs
        else:
            raise PermissionDenied


member_site.register(RegisterInvitationCode, RegisterInvitationCodeAdmin)
admin.site.register(RegisterInvitationCode, RegisterInvitationCodeAdmin)
management_site.register(RegisterInvitationCode, RegisterInvitationCodeAdmin)


class BankAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ['name', 'province', 'level', 'status', 'service_manager', 'create_date']

    def get_urls(self):
        urls = super(BankAdmin, self).get_urls()
        my_urls = patterns('',
                           (r'^register$', self.register_view),  # 会员注册
                           (r'^(.+)/confirm/$', self.confirm_view),  # 会员注册确认
                           (r'^(.+)/operator/$', self.operator_view),  # 查看修改执行人
                           (r'^(.+)/contactor/$', self.contactor_view),  # 查看修改执行人
                           (r'^(.+)/agreement/$', self.agreement_view),  # 查看战略&执行合作协议
        )
        return my_urls + urls

    def add_view(self, request, form_url='', extra_context=None):
        self.exclude = ['expired_date', 'invite_code', 'reference_count']
        if request.user.is_superuser or request.user.username == 'temp_register':
            return super(BankAdmin, self).add_view(request, form_url, extra_context)
        else:
            return HttpResponse('error: no privilige')

    @transaction.atomic
    def operator_view(self, request, object_id, form_url='', extra_context=None):
        '''
        查看修改执行人
        '''
        self.readonly_fields = []
        self.inlines = []
        if request.user.is_superuser:
            self.inlines = [BankContactorInline, BankOperatorConfirmInline]
            return super(BankAdmin, self).change_view(request, object_id, form_url, extra_context)

        self.change_form_template = 'member/member_change_form.html'
        user_profile = get_user_profile(request.user)
        group_name = None if user_profile is None else user_profile.groupname

        if not hasattr(user_profile, 'bank') or user_profile.bank_id != long(object_id):
            return HttpResponse('error: no privilege')  # 该联络人不属于该银行

        if group_name == BANK_CONTACTOR:
            self.exclude = ['strategic_agreements', 'level', 'execution_agreements', 'invite_code', 'expired_date', 'province', 'city', 'address', 'zipcode', 'fax_number',
                            'status', 'reference_count', 'referee_manager', 'service_manager', 'name']
            self.readonly_fields = ['short_name']
            operator_count = BankOperator.objects.filter(bank_id=long(object_id)).count()
            # 执行人不满3人，可增加
            if operator_count < 1:
                self.inlines = [BankOperatorAddInline]
            elif operator_count < 3:
                # todo 去掉 BankOperatorListInline 的 add another按钮
                self.inlines = [BankOperatorListInline, BankOperatorAddInline]
                pass
            else:
                self.inlines = [BankOperatorListInline]
        elif group_name == BANK_OPERATOR:
            self.exclude = ['strategic_agreements', 'level', 'execution_agreements', 'user', 'invite_code', 'groupname', 'province', 'city', 'address', 'zipcode', 'fax_number',
                            'status', 'reference_count', 'referee_manager', 'service_manager', 'name']
            self.readonly_fields = ['short_name']
            self.inlines = [BankOperatorListInline]
        # todo add other group here
        #elif group_name == MARKET_MANAGER or group_name == ZONE_MARKET:
        #elif group_name == SERVICE_MANAGER or group_name == ZONE_SERVICE:
        else:
            raise PermissionDenied

        to_field = request.POST.get(TO_FIELD_VAR, request.GET.get(TO_FIELD_VAR))
        if to_field and not self.to_field_allowed(request, to_field):
            raise DisallowedModelAdminToField("The field %s cannot be referenced." % to_field)

        model = self.model
        opts = model._meta
        add = object_id is None

        obj = self.get_object(request, unquote(object_id))

        if obj is None:
            raise Http404(_('%(name)s object with primary key %(key)r does not exist.') % {
                'name': force_text(opts.verbose_name), 'key': escape(object_id)})

        if request.method == 'POST' and "_saveasnew" in request.POST:
            return self.add_view(request, form_url=reverse('admin:%s_%s_add' % (
                opts.app_label, opts.model_name),
                                                           current_app=self.admin_site.name))

        ModelForm = self.get_form(request, obj)
        if request.method == 'POST':
            form = ModelForm(request.POST, request.FILES, instance=obj)
            if form.is_valid():
                form_validated = True
                new_object = self.save_form(request, form, change=not add)
            else:
                form_validated = False
                new_object = form.instance
            formsets, inline_instances = self._create_formsets(request, new_object)
            if all_valid(formsets) and form_validated:
                self.save_model(request, new_object, form, not add)
                # self.save_related(request, form, formsets, not add)
                form.save_m2m()
                for formset in formsets:
                    for inline_form in formset.forms:
                        if 'password1' in inline_form.cleaned_data:
                            operator_username = inline_form.cleaned_data['username']
                            operator_password = inline_form.cleaned_data['password1']
                            email = inline_form.cleaned_data['email']
                            # 创建执行人的django user
                            operator_user = User.objects.create_user(username=operator_username, password=operator_password, email=email)
                            group = Group.objects.get(name=BANK_OPERATOR)
                            operator_user.groups.clear()
                            operator_user.groups.add(group)
                            operator_user.is_active = True
                            operator_user.is_staff = True
                            operator_user.save()
                            inline_form.instance.user_id = operator_user.id
                            # inline_form.instance.groupname = BANK_OPERATOR
                        else:
                            if inline_form in formset.deleted_forms:
                                # formset.deleted_forms.remove(inline_form)
                                # inline_form.changed_data.remove('DELETE')
                                # inline_form.cleaned_data['DELETE'] = False
                                User.objects.filter(id=inline_form.instance.user_id).delete()
                    formset.save()

                change_message = self.construct_change_message(request, form, formsets)
                self.log_change(request, new_object, change_message)
                return self.response_change(request, new_object)
        else:
            form = ModelForm(instance=obj)
            formsets, inline_instances = self._create_formsets(request, obj)

        adminForm = helpers.AdminForm(
            form,
            list(self.get_fieldsets(request, obj)),
            self.get_prepopulated_fields(request, obj),
            self.get_readonly_fields(request, obj),
            model_admin=self)
        media = self.media + adminForm.media

        inline_formsets = self.get_inline_formsets(request, formsets, inline_instances, obj)
        for inline_formset in inline_formsets:
            media = media + inline_formset.media

        context = dict(self.admin_site.each_context(),
                       adminform=adminForm,
                       object_id=object_id,
                       original=obj,
                       to_field=to_field,
                       media=media,
                       is_popup=False,
                       inline_admin_formsets=inline_formsets,
                       errors=helpers.AdminErrorList(form, formsets),
                       preserved_filters=self.get_preserved_filters(request),
                       hide_inline=True,
        )

        bank = Bank.objects.get(id=long(object_id))

        extra_context = dict(self.admin_site.each_context(),
                             title=u'%s 执行人' % bank.name,
                             show_save=False,
        )
        context.update(extra_context or {})

        return self.render_change_form(request, context, add=add, change=not add, obj=obj, form_url=form_url)

    @transaction.atomic
    def contactor_view(self, request, object_id, form_url='', extra_context=None):
        '''
        查看修改执行人
        '''
        self.readonly_fields = []
        self.inlines = []
        if request.user.is_superuser:
            self.inlines = [BankContactorInline, BankOperatorConfirmInline]
            return super(BankAdmin, self).change_view(request, object_id, form_url, extra_context)

        self.change_form_template = 'member/member_change_form.html'

        user_profile = get_user_profile(request.user)
        group_name = None if user_profile is None else user_profile.groupname

        if not hasattr(user_profile, 'bank') or user_profile.bank_id != long(object_id):
            return HttpResponse('error: no privilege')  # 该联络人不属于该银行

        if group_name == BANK_CONTACTOR:
            self.exclude = ['strategic_agreements', 'execution_agreements', 'invite_code', 'expired_date', 'province', 'city', 'address', 'zipcode', 'fax_number', 'status',
                            'reference_count']
            self.readonly_fields = ['name', 'short_name']
            self.inlines = [BankContactorInline]
        elif group_name == BANK_OPERATOR:
            self.exclude = ['strategic_agreements', 'execution_agreements', 'invite_code', 'province', 'city', 'address', 'zipcode', 'fax_number', 'status', 'expired_date',
                            'reference_count']
            self.readonly_fields = ['name', 'short_name']
            self.inlines = [BankContactorReadonlyInline]

        bank = Bank.objects.get(id=long(object_id))

        extra_context = dict(self.admin_site.each_context(),
                             title=u'%s 主联络人' % bank.name,
        )

        return super(BankAdmin, self).change_view(request, object_id, form_url, extra_context)

    @transaction.atomic
    def agreement_view(self, request, object_id, form_url='', extra_context=None):
        '''
        查看修改执行人
        '''
        self.readonly_fields = ['name', 'service_manager', 'expired_date', 'create_date']
        self.inlines = []
        self.exclude = ['short_name', 'province', 'city', 'address', 'zipcode', 'fax_number', 'strategic_agreements', 'execution_agreements', 'level', 'status', 'invite_code',
                        'referee_manager', 'reference_count']
        self.change_form_template = None

        user_profile = get_user_profile(request.user)
        group_name = None if user_profile is None else user_profile.groupname

        if request.user.is_superuser:
            pass
        elif group_name == BANK_CONTACTOR or group_name == BANK_OPERATOR:
            self.change_form_template = 'member/bank_agreement_form.html'
            # self.inlines = [BankAttachmentInline]
            bank = Bank.objects.get(pk=object_id)
            strategic_agreements = BankAttachment.objects.filter(bank_id=object_id, type=STRATEGIC_AGREEMENT).order_by('-create_time')
            execution_agreements = BankAttachment.objects.filter(bank_id=object_id, type=EXECUTION_AGREEMENT).order_by('-create_time')
            extra_context = dict(self.admin_site.each_context(),
                                 title=u'[银行会员]%s 合作协议' % bank.short_name,
                                 hide_inline=False,
                                 bank_id=object_id,
                                 bank=bank,
                                 strategic_agreements=strategic_agreements,
                                 execution_agreements=execution_agreements,
                                 is_contactor=group_name == BANK_CONTACTOR,
                                 user_profile=user_profile,
            )
        return super(BankAdmin, self).change_view(request, object_id, form_url, extra_context)

    # If i comment these line service dashboard works well when user click bank type member
    # def changelist_view(self, request, extra_context=None):
    #     import ipdb; ipdb.set_trace()
    #     if request.user.is_superuser:
    #         return super(BankAdmin, self).changelist_view(request, extra_context)
    #     group_name = get_group(request.user)
    #     if group_name == BANK_CONTACTOR:
    #         return HttpResponse('error: no privilige')

    def change_view(self, request, object_id, form_url='', extra_context=None):
        self.readonly_fields = []
        self.inlines = []
        self.form = ModelForm
        if request.user.is_superuser:
            self.inlines = [BankContactorInline, BankOperatorConfirmInline]
            return super(BankAdmin, self).change_view(request, object_id, form_url, extra_context)

        user_profile = get_user_profile(request.user)
        group_name = None if user_profile is None else user_profile.groupname

        if group_name in (ZONE_MARKET, MARKET_MANAGER, ZONE_SERVICE, SERVICE_MANAGER, TOP_MANAGER):
            self.change_form_template = 'management/confirm_bank_form.html'
            self.inlines = [BankContactorInline]
            self.readonly_fields = ['level', 'status', 'invite_code', 'expired_date', 'reference_count', 'referee_manager']
        elif group_name == BANK_CONTACTOR:
            self.change_form_template = 'member/bank_display_form.html'
            self.inlines = [BankContactorInline]
            self.exclude = ['expired_date', 'invite_code', 'status', 'referee_manager']
            self.readonly_fields = ['level', 'reference_count', 'service_manager']
        elif group_name == BANK_OPERATOR:
            self.change_form_template = 'member/bank_display_form.html'
            self.inlines = [BankContactorReadonlyInline]
            self.exclude = ['expired_date', 'invite_code', 'status', 'strategic_agreements', 'execution_agreements', 'referee_manager']
            self.readonly_fields = ['name', 'short_name', 'province', 'city', 'address', 'zipcode', 'fax_number', 'level', 'reference_count', 'service_manager']
        else:
            raise PermissionDenied

        bank = Bank.objects.get(pk=object_id)
        strategic_agreements = BankAttachment.objects.filter(bank_id=object_id, type=STRATEGIC_AGREEMENT).order_by('-create_time')[:5]
        execution_agreements = BankAttachment.objects.filter(bank_id=object_id, type=EXECUTION_AGREEMENT).order_by('-create_time')[:5]
        extra_context = dict(self.admin_site.each_context(),
                             title=u'银行会员 %s' % bank.name,
                             strategic_agreements=strategic_agreements,
                             execution_agreements=execution_agreements,
                             hide_inline=False,
                             bank_id=object_id,
                             is_contactor=group_name == BANK_CONTACTOR,
                             user_profile=user_profile,
                             bank=bank,
        )

        return super(BankAdmin, self).change_view(request, object_id, form_url, extra_context)

    def has_register_permission(self, request):
        opts = self.opts
        codename = get_permission_codename('register', opts)
        return request.user.has_perm("%s.%s" % (opts.app_label, codename))

    def check_invinte_code(self, code):
        '''
        验证邀请码有效
        '''
        codes = RegisterInvitationCode.objects.filter(code=code)
        if codes.count() > 0 and codes[0].status == CODE_ACTIVATED and codes[0].member_type == BANK_MEMBER:
            return True
        return False

    @transaction.atomic
    def register_view(self, request, form_url='', extra_context=None):
        self.readonly_fields = []
        self.inlines = []
        if not "code" in request.GET:
            raise PermissionDenied

        invite_code_str = request.GET['code']
        # 验证邀请码
        if not self.check_invinte_code(invite_code_str):
            raise PermissionDenied
        # 检查邀请码
        invite_code = RegisterInvitationCode.objects.get(code=invite_code_str)
        if not invite_code.status == CODE_ACTIVATED:
            raise PermissionDenied

        self.form = BankRegisterForm
        self.exclude = ['status', 'invite_code', 'expired_date', 'level', 'reference_count', 'referee_manager', 'service_manager', 'execution_agreements', 'strategic_agreements']
        # self.inlines = [BankOperatorRegisterInline, ]
        self.add_form_template = 'member/register_form.html'
        user = authenticate(username='temp_register', password='temp_register')  # 会员注册专用用户
        request.user = user
        if not self.has_register_permission(request):
            raise PermissionDenied

        model = self.model
        opts = model._meta
        add = True
        obj = None
        object_id = None

        ModelForm = self.get_form(request, obj)

        if request.method == 'POST':
            invite_code_str = request.REQUEST.get('invite_code', None)
            if invite_code_str is None:
                raise PermissionDenied
            invite_code = RegisterInvitationCode.objects.get(code=invite_code_str)
            if not invite_code.status == CODE_ACTIVATED:
                raise PermissionDenied

            form = ModelForm(request.POST, request.FILES, instance=obj)
            if form.is_valid():
                form_validated = True
                new_object = self.save_form(request, form, change=not add)
            else:
                form_validated = False
                new_object = form.instance
            formsets, inline_instances = self._create_formsets(request, new_object)
            if all_valid(formsets) and form_validated:
                new_object.invite_code = invite_code
                # 推荐客服
                new_object.referee_manager = invite_code.market_manager
                self.save_model(request, new_object, form, not add)
                # 保存会员单位
                form.save_m2m()
                # todo 检查表单中主联络人username和执行人username不重复

                # save strategic_agreements_file and execution_agreements_file
                # new_object.strategic_agreements = request.FILES['strategic_agreements_file']
                # new_object.execution_agreements = request.FILES['execution_agreements_file']
                strategic_agreement = BankAttachment()
                strategic_agreement.bank_id = new_object.id
                strategic_agreement.file = request.FILES['strategic_agreements_file']
                strategic_agreement.type = STRATEGIC_AGREEMENT
                strategic_agreement.save()

                execution_agreement = BankAttachment()
                execution_agreement.bank_id = new_object.id
                execution_agreement.file = request.FILES['execution_agreements_file']
                execution_agreement.type = EXECUTION_AGREEMENT
                execution_agreement.save()

                # 添加每个执行人表单
                for formset in formsets:
                    for inline_form in formset.forms:
                        if isinstance(inline_form, BankOperatorForm):
                            operator_username = inline_form.instance.username
                            operator_password = inline_form.cleaned_data['password1']
                            # 创建执行人的django user
                            operator_user = User.objects.create_user(username=operator_username, password=operator_password, email=inline_form.instance.email)
                            group = Group.objects.get(name=BANK_OPERATOR)
                            operator_user.is_active = False
                            operator_user.groups.clear()
                            operator_user.groups.add(group)
                            operator_user.save()
                            inline_form.instance.user_id = operator_user.id
                            # inline_form.instance.groupname = BANK_OPERATOR
                            inline_form.instance.bank_id = new_object.id
                            inline_form.save()

                # 保存主联络人
                contactor = BankContactor()
                contactor.username = request.REQUEST.get('username')
                contactor.email = request.REQUEST.get('contactor_email')
                password = request.REQUEST.get('password1')
                # 创建主联络人django user
                user = User.objects.create_user(username=contactor.username, password=password, email=contactor.email)
                user.is_active = False
                group = Group.objects.get(name=BANK_CONTACTOR)
                user.groups.add(group)
                user.save()

                contactor.user_id = user.id
                contactor.bank_id = new_object.id
                # contactor.groupname = BANK_CONTACTOR
                contactor.name = request.REQUEST.get('contactor_name')
                contactor.identity_card = request.REQUEST.get('contactor_identity')
                contactor.mobile_number = request.REQUEST.get('contactor_mobile')
                contactor.pwd_question = request.REQUEST.get('contactor_question')
                contactor.pwd_answer = request.REQUEST.get('contactor_answer')
                contactor.save()

                invite_code.status = CODE_USED
                invite_code.used_date = datetime.datetime.now()
                invite_code.save()
                self.log_addition(request, new_object)
                return self.response_add(request, new_object)
        else:
            initial = self.get_changeform_initial_data(request)
            form = ModelForm(initial=initial)
            formsets, inline_instances = self._create_formsets(request, self.model())

        adminForm = helpers.AdminForm(
            form,
            list(self.get_fieldsets(request, obj)),
            self.get_prepopulated_fields(request, obj),
            self.get_readonly_fields(request, obj),
            model_admin=self)
        media = self.media + adminForm.media

        inline_formsets = self.get_inline_formsets(request, formsets, inline_instances, obj)
        for inline_formset in inline_formsets:
            media = media + inline_formset.media

        # BankOperatorFormSet = modelformset_factory(BankOperator)
        # formsets = BankOperatorFormSet()

        context = dict(self.admin_site.each_context(),
                       title=u'注册%s' % force_text(opts.verbose_name),
                       adminform=adminForm,
                       object_id=object_id,
                       original=obj,
                       is_popup=(IS_POPUP_VAR in request.POST or
                                 IS_POPUP_VAR in request.GET),
                       to_field=None,
                       media=media,
                       # formsets=formsets,
                       inline_admin_formsets=inline_formsets,
                       errors=helpers.AdminErrorList(form, formsets),
                       preserved_filters=self.get_preserved_filters(request),
                       invite_code=invite_code,
        )

        context.update(extra_context or {})

        # todo return register sucsess
        return self.render_change_form(request, context, add=add, change=not add, obj=obj, form_url=form_url)

    def confirm_view(self, request, object_id, form_url='', extra_context=None):
        # 仅有超级管理员和市场经理可以进行确认会员注册
        user_profile = get_user_profile(request.user)
        group_name = None if user_profile is None else user_profile.groupname

        bank = Bank.objects.get(pk=object_id)
        if not bank.status == MEMBER_PENDING:
            return render_to_response("management/notify.html", {
                "info": u'该银行已经通过审核',
                "title": u'该银行已审核',
                'user': request.user,
            })

        if request.user.is_superuser:
            pass
        elif group_name in (ZONE_MARKET, MARKET_MANAGER, TOP_MANAGER):
            pass
        else:
            return Http404

        self.inlines = [BankContactorInline, ]
        self.readonly_fields = ['invite_code', ]
        self.exclude = ['reference_count', 'status']
        self.form = ModelForm
        self.change_form_template = 'management/confirm_bank_form.html'

        strategic_agreements = BankAttachment.objects.filter(bank_id=object_id, type=STRATEGIC_AGREEMENT).order_by('-create_time')[:5]
        execution_agreements = BankAttachment.objects.filter(bank_id=object_id, type=EXECUTION_AGREEMENT).order_by('-create_time')[:5]
        extra_context = dict(self.admin_site.each_context(),
                             title=u'银行会员 %s' % bank.name,
                             strategic_agreements=strategic_agreements,
                             execution_agreements=execution_agreements,
                             hide_inline=False,
                             bank_id=object_id,
                             is_contactor=group_name == BANK_CONTACTOR,
                             user_profile=user_profile,
                             bank=bank,
        )

        result = super(BankAdmin, self).change_view(request, object_id, form_url, extra_context)
        # 添加成功才会返回HttpResponseRedirect，验证失败返回TemplateResponse
        if request.method == 'POST' and isinstance(result, HttpResponseRedirect):
            # 重置对用户的提醒信息
            request._messages = FallbackStorage(request)
            self.message_user(request, u'银行会员已审核通过', messages.SUCCESS)
            # 逻辑完成后返回changelist页面
            return super(BankAdmin, self).changelist_view(request, extra_context)

        return result

    def save_model(self, request, obj, form, change):
        if request.method == 'POST' and request.path.find('/confirm') > 0:
            # 确认注册成功状态
            bank = obj
            bank.status = MEMBER_ENABLED
            bank.save()
            # 激活所有联络人
            contactors = BankContactor.objects.filter(bank_id=bank.id).all()
            for contactor in contactors:
                contactor.user.is_active = True
                contactor.user.is_staff = True
                contactor.user.save()
                # operators = BankOperator.objects.filter(bank_id=bank.id).all()
                # for operator in operators:
                #     operator.is_active = True
                #     operator.save()
            #更新推荐会员数
            if bank.invite_code.referee_member_type == BANK_MEMBER and bank.invite_code.referee_member_id:
                referee = Bank.objects.get(id=bank.invite_code.referee_member_id)
                referee.reference_count += 1
            elif bank.invite_code.referee_member_type == ENTERPRISE_MEMBER and bank.invite_code.referee_member_id:
                referee = Enterprise.objects.get(id=bank.invite_code.referee_member_id)
                referee.reference_count += 1
        else:
            obj.save()

    def changelist_view(self, request, extra_context=None):
        self.list_display = ['name', 'province', 'level', 'status', 'service_manager', 'create_date']
        if request.user.is_superuser:
            return super(BankAdmin, self).changelist_view(request, extra_context)

        user_profile = get_user_profile(request.user)
        group_name = None if user_profile is None else user_profile.groupname

        # 只允许工作人员用户查看changelist
        title = u'全部银行会员'
        if isinstance(user_profile, Staff):
            pass
        else:
            return Http404

        if u'status__exact' in request.GET:
            status = request.GET[u'status__exact'].lower()
            if status == MEMBER_PENDING.lower():
                self.list_display = ['confirm_name_link', 'province', 'level', 'status', 'service_manager', 'create_date', 'confirm_button_link']
                title = u'待审核的银行注册'
            elif status == MEMBER_ENABLED.lower():
                title = u'已审核的银行注册'
            elif status == MEMBER_ENABLED.lower():
                title = u'已禁用的银行注册'
            elif status == MEMBER_EXPIRED.lower():
                title = u'已过期的银行注册'

        extra_context = dict(
            title=title,
        )
        return super(BankAdmin, self).changelist_view(request, extra_context)

    def get_queryset(self, request):
        qs = super(BankAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        user_profile = get_user_profile(request.user)
        group_name = None if user_profile is None else user_profile.groupname

        if group_name == BANK_CONTACTOR or group_name == BANK_OPERATOR:
            return qs.filter(id=user_profile.bank_id)
        elif isinstance(user_profile, Staff):
            return qs
        else:
            raise PermissionDenied


admin.site.register(Bank, BankAdmin)
member_site.register(Bank, BankAdmin)
management_site.register(Bank, BankAdmin)


class EnterpriseAdmin(admin.ModelAdmin):
    search_fields = ['name']
    inlines = [EnterpriseOperatorRegisterInline, ]
    list_display = ['name', 'province', 'level', 'status', 'service_manager', 'create_date']

    def get_urls(self):
        urls = super(EnterpriseAdmin, self).get_urls()
        my_urls = patterns('',
                           (r'^register/$', self.register_view),
                           (r'^(.+)/confirm/$', self.confirm_view),
                           (r'^(.+)/operator/$', self.operator_view),  # 查看修改执行人
                           (r'^(.+)/contactor/$', self.contactor_view),  # 查看修改执行人
                           (r'^(.+)/identification/$', self.identification_view),  # 查看企业资质
        )
        return my_urls + urls

    def add_view(self, request, form_url='', extra_context=None):
        self.exclude = ['expired_date', 'status', 'invite_code', 'reference_count']
        self.form = ModelForm
        return super(EnterpriseAdmin, self).add_view(request, form_url, extra_context)

    @transaction.atomic
    def operator_view(self, request, object_id, form_url='', extra_context=None):
        self.readonly_fields = []
        self.inlines = []
        if request.user.is_superuser:
            self.inlines = [EnterpriseContactorInline, EnterpriseOperatorConfirmInline]
            return super(EnterpriseAdmin, self).change_view(request, object_id, form_url, extra_context)

        self.change_form_template = 'member/member_change_form.html'
        user_profile = get_user_profile(request.user)
        group_name = None if user_profile is None else user_profile.groupname

        if not hasattr(user_profile, 'enterprise') or user_profile.enterprise_id != long(object_id):
            return HttpResponse('error: no privilege')  # 该联络人不属于该企业
        elif group_name == ENTERPRISE_CONTACTOR:
            self.exclude = ['licence', 'invite_code', 'expired_date', 'province', 'city', 'address', 'zipcode', 'fax_number', 'status', 'reference_count']
            self.readonly_fields = ['name', ]
            operator_count = EnterpriseOperator.objects.filter(enterprise_id=long(object_id)).count()
            # 执行人不满3人，可增加
            if operator_count < 1:
                self.inlines = [EnterpriseOperatorAddInline]
                pass
            else:
                # todo 去掉EnterpriseOperatorListInline的 add another按钮
                self.inlines = [EnterpriseOperatorListInline]
        elif group_name == ENTERPRISE_OPERATOR:
            self.exclude = ['licence', 'user', 'invite_code', 'province', 'city', 'address', 'zipcode', 'fax_number', 'status', 'reference_count']
            self.readonly_fields = ['name', ]
            self.inlines = [EnterpriseOperatorListInline]
            # todo add other group here
            #elif group_name == MARKET_MANAGER or group_name == ZONE_MARKET:
            #elif group_name == SERVICE_MANAGER or group_name == ZONE_SERVICE:
        else:
            raise PermissionDenied

        to_field = request.POST.get(TO_FIELD_VAR, request.GET.get(TO_FIELD_VAR))
        if to_field and not self.to_field_allowed(request, to_field):
            raise DisallowedModelAdminToField("The field %s cannot be referenced." % to_field)

        model = self.model
        opts = model._meta
        add = object_id is None

        obj = self.get_object(request, unquote(object_id))

        if obj is None:
            raise Http404(_('%(name)s object with primary key %(key)r does not exist.') % {
                'name': force_text(opts.verbose_name), 'key': escape(object_id)})

        if request.method == 'POST' and "_saveasnew" in request.POST:
            return self.add_view(request, form_url=reverse('admin:%s_%s_add' % (
                opts.app_label, opts.model_name),
                                                           current_app=self.admin_site.name))

        ModelForm = self.get_form(request, obj)
        if request.method == 'POST':
            form = ModelForm(request.POST, request.FILES, instance=obj)
            if form.is_valid():
                form_validated = True
                new_object = self.save_form(request, form, change=not add)
            else:
                form_validated = False
                new_object = form.instance
            formsets, inline_instances = self._create_formsets(request, new_object)
            if all_valid(formsets) and form_validated:
                self.save_model(request, new_object, form, not add)
                # self.save_related(request, form, formsets, not add)
                form.save_m2m()
                for formset in formsets:
                    for inline_form in formset.forms:
                        if 'password1' in inline_form.cleaned_data:
                            operator_username = inline_form.cleaned_data['username']
                            operator_password = inline_form.cleaned_data['password1']
                            email = inline_form.cleaned_data['email']
                            # 创建执行人的django user
                            operator_user = User.objects.create_user(username=operator_username, password=operator_password, email=email)
                            group = Group.objects.get(name=ENTERPRISE_OPERATOR)
                            operator_user.groups.clear()
                            operator_user.groups.add(group)
                            operator_user.is_active = True
                            operator_user.is_staff = True
                            operator_user.save()
                            inline_form.instance.user_id = operator_user.id
                            # inline_form.instance.groupname = ENTERPRISE_OPERATOR
                        else:
                            if inline_form in formset.deleted_forms:
                                # formset.deleted_forms.remove(inline_form)
                                # inline_form.changed_data.remove('DELETE')
                                # inline_form.cleaned_data['DELETE'] = False
                                User.objects.filter(id=inline_form.instance.user_id).delete()
                    formset.save()

                change_message = self.construct_change_message(request, form, formsets)
                self.log_change(request, new_object, change_message)
                return self.response_change(request, new_object)
        else:
            form = ModelForm(instance=obj)
            formsets, inline_instances = self._create_formsets(request, obj)

        adminForm = helpers.AdminForm(
            form,
            list(self.get_fieldsets(request, obj)),
            self.get_prepopulated_fields(request, obj),
            self.get_readonly_fields(request, obj),
            model_admin=self)
        media = self.media + adminForm.media

        inline_formsets = self.get_inline_formsets(request, formsets, inline_instances, obj)
        for inline_formset in inline_formsets:
            media = media + inline_formset.media

        context = dict(self.admin_site.each_context(),
                       adminform=adminForm,
                       object_id=object_id,
                       original=obj,
                       to_field=to_field,
                       media=media,
                       is_popup=False,
                       inline_admin_formsets=inline_formsets,
                       errors=helpers.AdminErrorList(form, formsets),
                       preserved_filters=self.get_preserved_filters(request),
        )

        enterprise = Enterprise.objects.get(id=long(object_id))

        extra_context = dict(self.admin_site.each_context(),
                             title=u'%s 执行人' % enterprise.name,
                             show_save=False,
        )
        context.update(extra_context or {})

        return self.render_change_form(request, context, add=add, change=not add, obj=obj, form_url=form_url)

    @transaction.atomic
    def contactor_view(self, request, object_id, form_url='', extra_context=None):
        self.readonly_fields = []
        self.inlines = []
        if request.user.is_superuser:
            self.inlines = [EnterpriseContactorInline, EnterpriseOperatorConfirmInline]
            return super(EnterpriseAdmin, self).change_view(request, object_id, form_url, extra_context)

        self.change_form_template = 'member/member_change_form.html'
        user_profile = get_user_profile(request.user)
        group_name = None if user_profile is None else user_profile.groupname

        if not hasattr(user_profile, 'enterprise') or user_profile.enterprise_id != long(object_id):
            return HttpResponse('error: no privilege')  # 该联络人不属于该企业
        elif group_name == ENTERPRISE_CONTACTOR:
            self.exclude = ['licence', 'invite_code', 'expired_date', 'province', 'city', 'address', 'zipcode', 'fax_number', 'status', 'reference_count']
            self.readonly_fields = ['name']
            self.inlines = [EnterpriseContactorInline]
        elif group_name == ENTERPRISE_OPERATOR:
            self.exclude = ['licence', 'invite_code', 'province', 'city', 'address', 'zipcode', 'fax_number', 'status', 'expired_date', 'reference_count']
            self.readonly_fields = ['name']
            self.inlines = [EnterpriseContactorReadonlyInline]
        else:
            raise PermissionDenied

        enterprise = Enterprise.objects.get(id=long(object_id))

        extra_context = dict(self.admin_site.each_context(),
                             title=u'%s 主联络人' % enterprise.name,
        )

        return super(EnterpriseAdmin, self).change_view(request, object_id, form_url, extra_context)

    @transaction.atomic
    def identification_view(self, request, object_id, form_url='', extra_context=None):
        '''
        查看修改执行人
        '''
        self.readonly_fields = ['name', 'service_manager', 'create_date']
        self.inlines = []
        self.exclude = ['short_name', 'province', 'city', 'address', 'zipcode', 'fax_number', 'level', 'status', 'invite_code',
                        'referee_manager', 'reference_count', 'licence', 'organization_code', 'tax_registration']
        self.change_form_template = None

        user_profile = get_user_profile(request.user)
        group_name = None if user_profile is None else user_profile.groupname

        if request.user.is_superuser:
            pass
        elif group_name == ENTERPRISE_CONTACTOR or group_name == ENTERPRISE_OPERATOR:
            self.change_form_template = 'member/enterprise_identification_form.html'
            enterprise = Enterprise.objects.get(pk=object_id)
            licences = EnterpriseAttachment.objects.filter(enterprise_id=object_id, type=LICENCE).order_by('-create_time')[:5]
            organization_codes = EnterpriseAttachment.objects.filter(enterprise_id=object_id, type=ORGANIZATION_CODE).order_by('-create_time')[:5]
            tax_registerations = EnterpriseAttachment.objects.filter(enterprise_id=object_id, type=TAX_REGISTRATION).order_by('-create_time')[:5]
            extra_context = dict(self.admin_site.each_context(),
                                 title=u'[企业会员]%s 企业资质' % enterprise.name,
                                 licences=licences,
                                 organization_codes=organization_codes,
                                 tax_registerations=tax_registerations,
                                 hide_inline=True,
                                 enterprise_id=object_id,
                                 enterprise=enterprise,
                                 is_contactor=group_name == ENTERPRISE_CONTACTOR,
                                 user_profile=user_profile,
            )

        return super(EnterpriseAdmin, self).change_view(request, object_id, form_url, extra_context)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        self.readonly_fields = ['reference_count']
        self.inlines = []
        self.exclude = []
        if request.user.is_superuser:
            self.inlines = [EnterpriseContactorInline, EnterpriseOperatorConfirmInline]
            return super(EnterpriseAdmin, self).change_view(request, object_id, form_url, extra_context)

        user_profile = get_user_profile(request.user)
        group_name = None if user_profile is None else user_profile.groupname

        if group_name in (ZONE_MARKET, MARKET_MANAGER, ZONE_SERVICE, SERVICE_MANAGER, TOP_MANAGER):
            self.inlines = [EnterpriseContactorInline, EnterpriseOperatorConfirmInline]
            self.readonly_fields = ['level', 'status', 'reference_count', 'referee_manager', 'invite_code']
            self.change_form_template = 'management/confirm_enterprise_form.html'
        elif group_name == ENTERPRISE_CONTACTOR:
            # todo replace with change_form.html
            self.change_form_template = 'member/enterprise_display_form.html'
            self.inlines = [EnterpriseContactorInline]
            self.exclude = ['expired_date', 'invite_code', 'status', 'referee_manager']
            self.readonly_fields = ['level', 'reference_count', 'service_manager']
        elif group_name == ENTERPRISE_OPERATOR:
            # todo replace with change_form.html
            self.change_form_template = 'member/enterprise_display_form.html'
            self.inlines = [EnterpriseContactorReadonlyInline]
            self.exclude = ['expired_date', 'invite_code', 'status', 'licence', 'referee_manager']
            self.readonly_fields = ['name', 'province', 'city', 'address', 'zipcode', 'fax_number', 'zipcode', 'level', 'reference_count', 'service_manager']
        else:
            raise PermissionDenied

        enterprise = Enterprise.objects.get(pk=object_id)
        licences = EnterpriseAttachment.objects.filter(enterprise_id=object_id, type=LICENCE).order_by('-create_time')[:5]
        organization_codes = EnterpriseAttachment.objects.filter(enterprise_id=object_id, type=ORGANIZATION_CODE).order_by('-create_time')[:5]
        tax_registerations = EnterpriseAttachment.objects.filter(enterprise_id=object_id, type=TAX_REGISTRATION).order_by('-create_time')[:5]
        extra_context = dict(self.admin_site.each_context(),
                             title=u'[企业会员]%s' % enterprise.name,
                             licences=licences,
                             organization_codes=organization_codes,
                             tax_registerations=tax_registerations,
                             hide_inline=True,
                             enterprise_id=object_id,
                             enterprise=enterprise,
                             is_contactor=group_name == ENTERPRISE_CONTACTOR,
                             user_profile=user_profile,
        )

        return super(EnterpriseAdmin, self).change_view(request, object_id, form_url, extra_context)

    def has_register_permission(self, request):
        opts = self.opts
        codename = get_permission_codename('register', opts)
        return request.user.has_perm("%s.%s" % (opts.app_label, codename))

    def check_invinte_code(self, code):
        '''
        验证邀请码有效
        '''
        codes = RegisterInvitationCode.objects.filter(code=code)
        if codes.count() > 0 and codes[0].status == CODE_ACTIVATED and codes[0].member_type == ENTERPRISE_MEMBER:
            return True
        return False

    @transaction.atomic
    def register_view(self, request, form_url='', extra_context=None):
        self.readonly_fields = []
        self.inlines = []
        if not "code" in request.GET:
            raise PermissionDenied

        invite_code = request.GET['code']
        # 验证邀请码
        if not self.check_invinte_code(invite_code):
            return render_to_response("member/notify.html", {
                "info": u'邀请码不正确或已使用',
                "title": u'邀请码不正确或已使用',
                'user': request.user,
            })

        user = authenticate(username='temp_register', password='temp_register')
        request.user = user
        if not self.has_register_permission(request):
            raise PermissionDenied

        self.form = EnterpriseRegisterForm
        # self.inlines = [EnterpriseOperatorRegisterInline, ]
        self.exclude = ['expired_date', 'status', 'invite_code', 'level', 'reference_count', 'referee_manager', 'service_manager', 'licence', 'organization_code',
                        'tax_registration']
        self.add_form_template = 'member/register_form.html'

        model = self.model
        opts = model._meta
        add = True
        obj = None
        object_id = None

        ModelForm = self.get_form(request, obj)
        if request.method == 'POST':
            invite_code_str = request.REQUEST.get('code', None)
            if invite_code_str is None:
                raise PermissionDenied

            # 检查邀请码
            invite_code = RegisterInvitationCode.objects.get(code=invite_code_str)
            if not invite_code.status == CODE_ACTIVATED:
                raise PermissionDenied

            form = ModelForm(request.POST, request.FILES, instance=obj)
            if form.is_valid():
                form_validated = True
                new_object = self.save_form(request, form, change=not add)
            else:
                form_validated = False
                new_object = form.instance
            formsets, inline_instances = self._create_formsets(request, new_object)
            if all_valid(formsets) and form_validated:
                new_object.invite_code = invite_code
                # 推荐客服
                new_object.referee_manager = invite_code.market_manager
                self.save_model(request, new_object, form, not add)
                # 保存会员单位
                form.save_m2m()
                # todo 检查表单中主联络人username和执行人username不重复

                # save licence_file, organization_code_file, tax_registration_file
                licence = EnterpriseAttachment()
                licence.enterprise_id = new_object.id
                licence.file = request.FILES['licence_file']
                licence.type = LICENCE
                licence.save()

                organization_code = EnterpriseAttachment()
                organization_code.enterprise_id = new_object.id
                organization_code.file = request.FILES['organization_code_file']
                organization_code.type = ORGANIZATION_CODE
                organization_code.save()

                tax_registration = EnterpriseAttachment()
                tax_registration.enterprise_id = new_object.id
                tax_registration.file = request.FILES['tax_registration_file']
                tax_registration.type = TAX_REGISTRATION
                tax_registration.save()

                # 添加每个执行人表单
                for formset in formsets:
                    for inline_form in formset.forms:
                        if isinstance(inline_form, EnterpriseOperatorForm):
                            operator_username = inline_form.instance.username
                            operator_password = inline_form.cleaned_data[0]['password1']
                            # 创建执行人的django user
                            operator_user = User.objects.create_user(username=operator_username, password=operator_password, email=inline_form.instance.email)
                            group = Group.objects.get(name=ENTERPRISE_OPERATOR)
                            operator_user.groups.clear()
                            operator_user.groups.add(group)
                            operator_user.is_active = False
                            operator_user.is_staff = False
                            operator_user.save()
                            inline_form.instance.user_id = operator_user.id
                            inline_form.instance.bank_id = new_object.id
                            # inline_form.instance.groupname = ENTERPRISE_OPERATOR
                            inline_form.save()

                # 添加主联络人
                contactor = EnterpriseContactor()
                contactor.username = request.REQUEST.get('username')
                contactor.email = request.REQUEST.get('contactor_email')
                password = request.REQUEST.get('password1')
                # 创建django user
                user = User.objects.create_user(username=contactor.username, password=password, email=contactor.email)
                user.is_active = False
                group = Group.objects.get(name=ENTERPRISE_CONTACTOR)
                user.groups.add(group)
                user.save()

                contactor.user_id = user.id
                contactor.enterprise_id = new_object.id
                # contactor.groupname = ENTERPRISE_CONTACTOR
                contactor.name = request.REQUEST.get('contactor_name')
                contactor.identity_card = request.REQUEST.get('contactor_identity')
                contactor.mobile_number = request.REQUEST.get('contactor_mobile')
                contactor.pwd_question = request.REQUEST.get('contactor_question')
                contactor.pwd_answer = request.REQUEST.get('contactor_answer')
                contactor.save()

                invite_code.status = CODE_USED
                invite_code.used_date = datetime.datetime.now()
                invite_code.save()
                if add:
                    self.log_addition(request, new_object)
                    # todo 修改注册成功通知页面
                    return self.response_add(request, new_object)
        else:
            if add:
                initial = self.get_changeform_initial_data(request)
                form = ModelForm(initial=initial)
                formsets, inline_instances = self._create_formsets(request, self.model())

        adminForm = helpers.AdminForm(
            form,
            list(self.get_fieldsets(request, obj)),
            self.get_prepopulated_fields(request, obj),
            self.get_readonly_fields(request, obj),
            model_admin=self)
        media = self.media + adminForm.media

        inline_formsets = self.get_inline_formsets(request, formsets, inline_instances, obj)
        for inline_formset in inline_formsets:
            media = media + inline_formset.media

        context = dict(self.admin_site.each_context(),
                       title=(_('Add %s') if add else _('Change %s')) % force_text(opts.verbose_name),
                       adminform=adminForm,
                       object_id=object_id,
                       original=obj,
                       is_popup=(IS_POPUP_VAR in request.POST or
                                 IS_POPUP_VAR in request.GET),
                       to_field=None,
                       media=media,
                       inline_admin_formsets=inline_formsets,
                       errors=helpers.AdminErrorList(form, formsets),
                       preserved_filters=self.get_preserved_filters(request),
                       invite_code=invite_code,
        )

        context.update(extra_context or {})

        # todo return register sucsess
        return self.render_change_form(request, context, add=add, change=not add, obj=obj, form_url=form_url)

    @transaction.atomic
    def confirm_view(self, request, object_id, form_url='', extra_context=None):
        # 仅有超级管理员和市场经理可以进行确认会员注册
        user_profile = get_user_profile(request.user)
        group_name = None if user_profile is None else user_profile.groupname

        enterprise = Enterprise.objects.get(pk=object_id)
        if not enterprise.status == MEMBER_PENDING:
            return render_to_response("management/notify.html", {
                "info": u'该企业已经通过审核',
                "title": u'该企业已审核',
                'user': request.user,
            })

        if request.user.is_superuser:
            pass
        elif group_name in (ZONE_MARKET, MARKET_MANAGER, TOP_MANAGER):
            pass
        else:
            return Http404

        self.inlines = [EnterpriseContactorInline, ]
        self.readonly_fields = ['invite_code', ]
        self.exclude = ['reference_count', 'status']
        self.form = ModelForm

        licences = EnterpriseAttachment.objects.filter(enterprise_id=object_id, type=LICENCE).order_by('-create_time')[:5]
        organization_codes = EnterpriseAttachment.objects.filter(enterprise_id=object_id, type=ORGANIZATION_CODE).order_by('-create_time')[:5]
        tax_registerations = EnterpriseAttachment.objects.filter(enterprise_id=object_id, type=TAX_REGISTRATION).order_by('-create_time')[:5]
        extra_context = dict(self.admin_site.each_context(),
                             title=u'[企业会员]%s' % enterprise.name,
                             licences=licences,
                             organization_codes=organization_codes,
                             tax_registerations=tax_registerations,
                             hide_inline=False,
                             enterprise_id=object_id,
                             enterprise=enterprise,
                             is_contactor=group_name == ENTERPRISE_CONTACTOR,
                             user_profile=user_profile,
        )
        self.change_form_template = 'management/confirm_enterprise_form.html'

        result = super(EnterpriseAdmin, self).change_view(request, object_id, form_url, extra_context)
        # 添加成功才会返回HttpResponseRedirect，验证失败返回TemplateResponse
        if request.method == 'POST' and isinstance(result, HttpResponseRedirect):
            # 重置对用户的提醒信息
            request._messages = FallbackStorage(request)
            self.message_user(request, u'企业会员已审核通过', messages.SUCCESS)
            # 逻辑完成后返回changelist页面
            return super(EnterpriseAdmin, self).changelist_view(request, extra_context)

        return super(EnterpriseAdmin, self).change_view(request, object_id, form_url, extra_context)

    def save_model(self, request, obj, form, change):
        # only for member confirm page
        if request.method == 'POST' and request.path.find('/confirm') > 0:
            # 确认注册成功状态
            enterprise = obj
            enterprise.status = MEMBER_ENABLED
            enterprise.save()
            # 激活所有联络人
            contactors = EnterpriseContactor.objects.filter(enterprise_id=enterprise.id).all()
            for contactor in contactors:
                contactor.user.is_active = True
                contactor.user.is_staff = True
                contactor.user.save()
            #更新推荐会员数
            if enterprise.invite_code.referee_member_type == BANK_MEMBER and enterprise.invite_code.referee_member_id:
                referee = Bank.objects.get(id=enterprise.invite_code.referee_member_id)
                referee.reference_count += 1
            elif enterprise.invite_code.referee_member_type == ENTERPRISE_MEMBER and enterprise.invite_code.referee_member_id:
                referee = Enterprise.objects.get(id=enterprise.invite_code.referee_member_id)
                referee.reference_count += 1
        else:
            obj.save()

    def changelist_view(self, request, extra_context=None):
        self.list_display = ['name', 'province', 'level', 'status', 'service_manager', 'create_date']
        if request.user.is_superuser:
            # todo
            # self.list_display = ['user', 'bank', 'name', 'mobile_number', 'email', 'create_date', 'last_login']
            return super(EnterpriseAdmin, self).changelist_view(request, extra_context)

        user_profile = get_user_profile(request.user)
        group_name = None if user_profile is None else user_profile.groupname

        # 只允许工作人员用户查看changelist
        if isinstance(user_profile, Staff):
            pass
        else:
            return Http404

        title = u'全部企业会员'
        if u'status__exact' in request.GET:
            status = request.GET[u'status__exact'].lower()
            if status == MEMBER_PENDING.lower():
                self.list_display = ['confirm_name_link', 'province', 'level', 'status', 'service_manager', 'create_date', 'confirm_button_link']
                title = u'待审核的企业注册'
            elif status == MEMBER_ENABLED.lower():
                title = u'已审核的企业注册'
            elif status == MEMBER_ENABLED.lower():
                title = u'已禁用的企业注册'
            elif status == MEMBER_EXPIRED.lower():
                title = u'已过期的企业注册'

        extra_context = dict(
            title=title,
        )
        return super(EnterpriseAdmin, self).changelist_view(request, extra_context)

    def get_queryset(self, request):
        qs = super(EnterpriseAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        user_profile = get_user_profile(request.user)
        group_name = None if user_profile is None else user_profile.groupname

        if group_name == ENTERPRISE_OPERATOR or group_name == ENTERPRISE_CONTACTOR:
            return qs.filter(id=user_profile.enterprise_id)
        elif isinstance(user_profile, Staff):
            return qs
        else:
            raise PermissionDenied


admin.site.register(Enterprise, EnterpriseAdmin)
member_site.register(Enterprise, EnterpriseAdmin)
management_site.register(Enterprise, EnterpriseAdmin)


class BankOperatorAdmin(admin.ModelAdmin):
    search_fields = ['name', 'username']

    def changelist_view(self, request, extra_context=None):
        if request.user.is_superuser:
            self.list_display = ['user', 'bank', 'name', 'mobile_number', 'email', 'create_date', 'last_login']
            return super(BankOperatorAdmin, self).changelist_view(request, extra_context)

        user_profile = get_user_profile(request.user)
        group_name = None if user_profile is None else user_profile.groupname

        # 只允许工作人员用户查看changelist
        if isinstance(user_profile, Staff) or group_name == BANK_CONTACTOR:
            pass
        else:
            return Http404

        extra_context = dict(
            user_profile=user_profile,
        )
        return super(BankOperatorAdmin, self).changelist_view(request, extra_context)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        self.exclude = []
        self.readonly_fields = []
        self.inlines = []

        if request.user.is_superuser:
            return super(BankOperatorAdmin, self).change_view(request, object_id, form_url, extra_context)

        user_profile = get_user_profile(request.user)
        group_name = None if user_profile is None else user_profile.groupname

        if group_name == BANK_CONTACTOR:
            obj = BankOperator.objects.get(id=long(object_id))
            if not user_profile.bank_id == obj.bank_id:
                raise PermissionDenied
            self.exclude = ['user', 'groupname', 'last_login', 'modify_date']
            self.readonly_fields = ['name', 'username', 'bank', 'identity_card', 'mobile_number', 'telephone', 'email', 'position']
        elif group_name == BANK_OPERATOR:
            # 不允许查看其它执行人
            if not user_profile.id == long(object_id):
                raise PermissionDenied
            self.exclude = ['user', 'groupname', 'last_login', 'modify_date']
            self.readonly_fields = ['bank', 'username']
        elif group_name == ZONE_SERVICE or group_name == SERVICE_MANAGER:
            # todo 客服查看执行人
            pass
        else:
            raise PermissionDenied
        extra_context = dict(
            user_profile=user_profile,
        )
        return super(BankOperatorAdmin, self).change_view(request, object_id, form_url, extra_context)

    def get_queryset(self, request):
        qs = super(BankOperatorAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        user_profile = get_user_profile(request.user)
        group_name = None if user_profile is None else user_profile.groupname

        if group_name == BANK_CONTACTOR:
            return qs.filter(bank_id=user_profile.bank_id)
        elif group_name == BANK_OPERATOR:
            return qs.filter(id=user_profile.id)
        elif isinstance(user_profile, Staff):
            return qs
        else:
            raise PermissionDenied


admin.site.register(BankOperator, BankOperatorAdmin)
member_site.register(BankOperator, BankOperatorAdmin)
management_site.register(BankOperator, BankOperatorAdmin)


class BankContactorAdmin(admin.ModelAdmin):
    search_fields = ['name', 'username']

    def changelist_view(self, request, extra_context=None):
        if request.user.is_superuser:
            self.list_display = ['user', 'bank', 'name', 'mobile_number', 'email', 'create_date', 'last_login']
            return super(BankContactorAdmin, self).changelist_view(request, extra_context)

        user_profile = get_user_profile(request.user)
        group_name = None if user_profile is None else user_profile.groupname

        # 只允许工作人员用户查看changelist
        if isinstance(user_profile, Staff):
            pass
        else:
            return Http404

        extra_context = dict(
            user_profile=user_profile,
        )
        return super(BankContactorAdmin, self).changelist_view(request, extra_context)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        self.exclude = []
        self.readonly_fields = []
        self.inlines = []

        if request.user.is_superuser:
            return super(BankContactorAdmin, self).change_view(request, object_id, form_url, extra_context)

        user_profile = get_user_profile(request.user)
        group_name = None if user_profile is None else user_profile.groupname

        if group_name == BANK_CONTACTOR:
            # 不允许查看其它主联络人
            if not user_profile.id == long(object_id):
                return PermissionDenied
            self.exclude = ['user', 'groupname', 'last_login', 'modify_date']
            self.readonly_fields = ['bank', 'username']
        elif group_name == BANK_OPERATOR:
            obj = BankContactor.objects.get(id=long(object_id))
            if not user_profile.bank_id == obj.bank_id:
                raise PermissionDenied
            # 执行人只能查看主联络人的信息
            self.exclude = ['user', 'groupname', 'last_login', 'modify_date']
            self.readonly_fields = ['name', 'username', 'bank', 'identity_card', 'mobile_number', 'telephone', 'email', 'position']
        elif group_name == ZONE_SERVICE or group_name == SERVICE_MANAGER:
            # todo 客服查看执行人
            pass
        else:
            raise PermissionDenied

        extra_context = dict(
            user_profile=user_profile,
        )
        return super(BankContactorAdmin, self).change_view(request, object_id, form_url, extra_context)

    def get_queryset(self, request):
        qs = super(BankContactorAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        user_profile = get_user_profile(request.user)
        group_name = None if user_profile is None else user_profile.groupname

        if group_name == BANK_CONTACTOR:
            return qs.filter(id=user_profile.id)
        elif group_name == BANK_OPERATOR:
            return qs.filter(bank_id=user_profile.bank_id)
        elif isinstance(user_profile, Staff):
            return qs
        else:
            raise PermissionDenied


admin.site.register(BankContactor, BankContactorAdmin)
member_site.register(BankContactor, BankContactorAdmin)
management_site.register(BankContactor, BankContactorAdmin)


class EnterpriseContactorAdmin(admin.ModelAdmin):
    search_fields = ['name', 'username']

    def changelist_view(self, request, extra_context=None):
        if request.user.is_superuser:
            self.list_display = ['user', 'enterprise', 'name', 'mobile_number', 'email', 'create_date', 'last_login']
            return super(EnterpriseContactorAdmin, self).changelist_view(request, extra_context)

        user_profile = get_user_profile(request.user)
        group_name = None if user_profile is None else user_profile.groupname

        # 只允许工作人员用户查看changelist
        if isinstance(user_profile, Staff):
            pass
        else:
            return Http404

        extra_context = dict(
            user_profile=user_profile,
        )
        return super(EnterpriseContactorAdmin, self).changelist_view(request, extra_context)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        self.exclude = []
        self.readonly_fields = []
        self.inlines = []

        if request.user.is_superuser:
            return super(EnterpriseContactorAdmin, self).change_view(request, object_id, form_url, extra_context)

        user_profile = get_user_profile(request.user)
        group_name = None if user_profile is None else user_profile.groupname

        if group_name == ENTERPRISE_CONTACTOR:
            # 不允许查看其它会员单位的主联络人
            if not user_profile.id == long(object_id):
                raise PermissionDenied
            self.exclude = ['user', 'groupname', 'last_login', 'modify_date']
            self.readonly_fields = ['enterprise', 'username']
        elif group_name == ENTERPRISE_OPERATOR:
            # 不允许查看其它会员单位的执行人
            obj = EnterpriseOperator.objects.get(id=long(object_id))
            if not user_profile.enterprise_id == obj.enterprise_id:
                raise PermissionDenied
            self.exclude = ['user', 'groupname', 'last_login', 'modify_date']
            self.readonly_fields = ['enterprise', 'username']['name', 'username', 'enterprise', 'identity_card', 'mobile_number', 'telephone', 'email', 'position']
        elif group_name == ZONE_SERVICE or group_name == SERVICE_MANAGER:
            # todo 客服查看执行人
            pass
        else:
            raise PermissionDenied

        extra_context = dict(
            user_profile=user_profile,
        )
        return super(EnterpriseContactorAdmin, self).change_view(request, object_id, form_url, extra_context)

    def get_queryset(self, request):
        qs = super(EnterpriseContactorAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        user_profile = get_user_profile(request.user)
        group_name = None if user_profile is None else user_profile.groupname

        if group_name == ENTERPRISE_CONTACTOR:
            return qs.filter(id=user_profile.id)
        elif group_name == ENTERPRISE_OPERATOR:
            return qs.filter(enterprise_id=user_profile.enterprise_id)
        elif isinstance(user_profile, Staff):
            return qs
        else:
            raise PermissionDenied


admin.site.register(EnterpriseContactor, EnterpriseContactorAdmin)
member_site.register(EnterpriseContactor, EnterpriseContactorAdmin)
management_site.register(EnterpriseContactor, EnterpriseContactorAdmin)


class EnterpriseOperatorAdmin(admin.ModelAdmin):
    search_fields = ['name', 'username']

    def changelist_view(self, request, extra_context=None):
        if request.user.is_superuser:
            self.list_display = ['user', 'enterprise', 'name', 'mobile_number', 'email', 'create_date', 'last_login']
            return super(EnterpriseOperatorAdmin, self).changelist_view(request, extra_context)

        user_profile = get_user_profile(request.user)
        group_name = None if user_profile is None else user_profile.groupname

        # 只允许工作人员用户查看changelist
        if isinstance(user_profile, Staff) or group_name == ENTERPRISE_CONTACTOR:
            pass
        else:
            return Http404

        extra_context = dict(
            user_profile=user_profile,
        )
        return super(EnterpriseOperatorAdmin, self).changelist_view(request, extra_context)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        self.exclude = []
        self.readonly_fields = []
        self.inlines = []

        if request.user.is_superuser:
            return super(EnterpriseOperatorAdmin, self).change_view(request, object_id, form_url, extra_context)

        user_profile = get_user_profile(request.user)
        group_name = None if user_profile is None else user_profile.groupname

        if group_name == ENTERPRISE_CONTACTOR:
            obj = EnterpriseOperator.objects.get(id=long(object_id))
            if not user_profile.enterprise_id == obj.enterprise_id:
                raise PermissionDenied
            self.exclude = ['user', 'groupname', 'last_login', 'modify_date']
            self.readonly_fields = ['name', 'username', 'enterprise', 'identity_card', 'mobile_number', 'telephone', 'email', 'position']
        elif group_name == ENTERPRISE_OPERATOR:
            # 不允许查看其它执行人
            if not user_profile.id == long(object_id):
                raise PermissionDenied
            self.exclude = ['user', 'groupname', 'last_login', 'modify_date']
            self.readonly_fields = ['enterprise', 'username']
        elif group_name == ZONE_SERVICE or group_name == SERVICE_MANAGER:
            # todo 客服查看执行人
            pass
        else:
            raise PermissionDenied

        extra_context = dict(
            user_profile=user_profile,
        )
        return super(EnterpriseOperatorAdmin, self).change_view(request, object_id, form_url, extra_context)

    def get_queryset(self, request):
        qs = super(EnterpriseOperatorAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        user_profile = get_user_profile(request.user)
        group_name = None if user_profile is None else user_profile.groupname

        if group_name == ENTERPRISE_CONTACTOR:
            return qs.filter(enterprise_id=user_profile.enterprise_id)
        elif group_name == ENTERPRISE_OPERATOR:
            return qs.filter(id=user_profile.id)
        elif isinstance(user_profile, Staff):
            return qs
        else:
            raise PermissionDenied


admin.site.register(EnterpriseOperator, EnterpriseOperatorAdmin)
member_site.register(EnterpriseOperator, EnterpriseOperatorAdmin)
management_site.register(EnterpriseOperator, EnterpriseOperatorAdmin)


class EnterpriseAttachmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'enterprise', 'type', 'get_link', 'get_thumbnail_link']

    @transaction.atomic
    def add_view(self, request, form_url='', extra_context=None):
        user_profile = get_user_profile(request.user)
        group_name = None if user_profile is None else user_profile.groupname

        if request.user.is_superuser:
            self.exclude = []
            self.readonly_fields = []
        elif group_name == ENTERPRISE_CONTACTOR or group_name == ENTERPRISE_OPERATOR:
            self.exclude = ['name', 'enterprise', 'extension', 'size', 'width', 'height', 'thumbnail', 'creator', 'need_login']
            self.readonly_fields = []
            self.change_form_template = 'member/member_change_form.html'

            if request.method == 'POST':
                self.exclude.remove('enterprise')
                self.exclude.remove('creator')
                mutable = request.POST._mutable
                request.POST._mutable = True
                request.POST['bank'] = user_profile.bank.id
                request.POST['creator'] = request.user.id
                request.POST._mutable = mutable
        elif group_name == SERVICE_MANAGER or group_name == ZONE_SERVICE:
            self.exclude = ['name', 'extension', 'size', 'width', 'height', 'thumbnail', 'creator']
            self.readonly_fields = []

        return super(EnterpriseAttachmentAdmin, self).add_view(request, form_url, extra_context)

    @transaction.atomic
    def change_view(self, request, object_id, form_url='', extra_context=None):
        if request.user.is_superuser:
            self.exclude = []
            self.readonly_fields = []
        else:
            self.exclude = []
            self.readonly_fields = ['name', 'extension', 'size', 'width', 'height', 'thumbnail']
        return super(EnterpriseAttachmentAdmin, self).change_view(request, object_id, form_url, extra_context)

    def get_queryset(self, request):
        qs = super(EnterpriseAttachmentAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        user_profile = get_user_profile(request.user)
        group_name = None if user_profile is None else user_profile.groupname

        if group_name == ENTERPRISE_CONTACTOR or group_name == ENTERPRISE_OPERATOR:
            return qs.filter(enterprise_id=user_profile.enterprise_id)
        elif isinstance(user_profile, Staff):
            return qs
        else:
            raise PermissionDenied


admin.site.register(EnterpriseAttachment, EnterpriseAttachmentAdmin)
member_site.register(EnterpriseAttachment, EnterpriseAttachmentAdmin)
management_site.register(EnterpriseAttachment, EnterpriseAttachmentAdmin)


class BankAttachmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'type', 'get_link', 'get_thumbnail_link']

    @transaction.atomic
    def add_view(self, request, form_url='', extra_context=None):
        # self.form = ModelForm
        user_profile = get_user_profile(request.user)
        group_name = None if user_profile is None else user_profile.groupname

        if request.user.is_superuser:
            self.exclude = []
            self.readonly_fields = []
        elif group_name == BANK_CONTACTOR or group_name == BANK_OPERATOR:
            self.exclude = ['name', 'bank', 'extension', 'size', 'width', 'height', 'thumbnail', 'creator', 'need_login']
            self.readonly_fields = []
            self.change_form_template = 'member/member_change_form.html'

            if request.method == 'POST':
                self.exclude.remove('bank')
                self.exclude.remove('creator')
                mutable = request.POST._mutable
                request.POST._mutable = True
                request.POST['bank'] = user_profile.bank.id
                request.POST['creator'] = request.user.id
                request.POST._mutable = mutable
        elif group_name == SERVICE_MANAGER or group_name == ZONE_SERVICE:
            self.exclude = ['name', 'extension', 'size', 'width', 'height', 'thumbnail', 'creator']
            self.readonly_fields = []
            # todo

        return super(BankAttachmentAdmin, self).add_view(request, form_url, extra_context)

    @transaction.atomic
    def change_view(self, request, object_id, form_url='', extra_context=None):
        if request.user.is_superuser:
            self.exclude = []
            self.readonly_fields = []
        else:
            self.exclude = []
            self.readonly_fields = ['name', 'extension', 'size', 'width', 'height', 'thumbnail']
        return super(BankAttachmentAdmin, self).change_view(request, object_id, form_url, extra_context)

        # def save_model(self, request, obj, form, change):
        #     if request.method == 'POST':
        #         pass
        #     super(BankAttachmentAdmin, self).save_model(request, obj, form, change)

    def get_queryset(self, request):
        qs = super(BankAttachmentAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        user_profile = get_user_profile(request.user)
        group_name = None if user_profile is None else user_profile.groupname

        if group_name == BANK_CONTACTOR or group_name == BANK_OPERATOR:
            return qs.filter(bank_id=user_profile.bank_id)
        elif isinstance(user_profile, Staff):
            return qs
        else:
            raise PermissionDenied


admin.site.register(BankAttachment, BankAttachmentAdmin)
member_site.register(BankAttachment, BankAttachmentAdmin)
management_site.register(BankAttachment, BankAttachmentAdmin)










