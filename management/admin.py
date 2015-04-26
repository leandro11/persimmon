#coding=utf-8
import random, datetime
import sys

from django.contrib import admin
from django.forms import ModelForm
from django.contrib.auth.models import User, Group
from django.db import transaction
from django.http import HttpResponse
from django.contrib.admin import widgets, helpers
from django.utils.encoding import force_text, python_2_unicode_compatible
from django.conf.urls import patterns
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from django.forms.formsets import all_valid
from django.utils.translation import ugettext as _
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_permission_codename
from django.core.exceptions import (
    PermissionDenied, ValidationError, FieldError, ImproperlyConfigured)
from django.contrib.admin.utils import (
    quote, unquote, flatten_fieldsets, get_deleted_objects, model_format_dict,
    NestedObjects, lookup_needs_distinct)
from django.forms.models import (
    modelform_factory, modelformset_factory, inlineformset_factory,
    BaseInlineFormSet, modelform_defines_fields)
from django.utils.crypto import get_random_string
from django import forms
from django.core import validators
from django.http import Http404, HttpResponseRedirect
from django.contrib.admin.exceptions import DisallowedModelAdminToField
from django.utils.html import escape, escapejs
from django.core.urlresolvers import reverse

from management.models import (Zone, Province, Staff)
from management.sites import site as management_site
from management.form import StaffRegisterForm


reload(sys)
sys.setdefaultencoding('utf-8')

csrf_protect_m = method_decorator(csrf_protect)
IS_POPUP_VAR = '_popup'
TO_FIELD_VAR = '_to_field'

# Temp user only for registing of staff in company
STAFF_REGISTER = authenticate(username='staff_register', password='staff_register')


class ProvinceInline(admin.TabularInline):
    model = Province
    extra = 0
    can_delete = True
    exclude = []
    verbose_name = u'省份'
    verbose_name_plural = u'省份'


class ProvinceAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

admin.site.register(Province, ProvinceAdmin)
management_site.register(Province, ProvinceAdmin)


class ZoneAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'name',)
    search_fields = ('name',)
    list_editable = ('name',)
    # inlines = [ProvinceInline, ]

admin.site.register(Zone, ZoneAdmin)
management_site.register(Zone, ZoneAdmin)


class StaffAdmin(admin.ModelAdmin):
    search_fields = ['name']
    readonly_fields = []
    inlines = []
    form = StaffRegisterForm
    exclude = ['user']
    add_form_template = 'management/register_form.html'

    def get_urls(self):
        urls = super(StaffAdmin, self).get_urls()
        my_urls = patterns('',
                           (r'^register/$', self.register_view),  # 工作人员注册
        )
        return my_urls + urls

    def add_view(self, request, form_url='', extra_context=None):
        if request.user.is_superuser:
            self.exclude = []
            return super(StaffAdmin, self).add_view(request, form_url, extra_context)
        self.exclude = ['user']
        self.form = ModelForm
        return super(StaffAdmin, self).add_view(request, form_url, extra_context)

    def has_change_permission(self, request, obj=None):
        opts = self.opts
        codename = get_permission_codename('change', opts)
        return request.user.has_perm("%s.%s" % (opts.app_label, codename))

    def change_view(self, request, object_id, form_url='', extra_context=None):
        if request.user.is_active:
            self.exclude = []
            return super(StaffAdmin, self).change_view(request, object_id, form_url, extra_context)

    def save_model(self, request, obj, form, change):
        # give supper admin privilege
        if request.method == 'POST' and request.path.find('/register') > 0:
            username = request.REQUEST.get('username')
            password = request.REQUEST.get('password1')

            user = User.objects.create_user(username=username,
                                            password=password,
                                            email=obj.email)
            user.is_staff = True
            user.is_staff = True
            user.groups.clear()
            group = Group.objects.get(name=obj.position)
            if not group:
                raise Exception("No group obj for position: %s" % obj.position)
            user.groups.add(group)
            user.save()
            obj.user = user
            obj.save()          # Save model

    @transaction.atomic
    def register_view(self, request, form_url='', extra_context=None):
        request.user = STAFF_REGISTER
        ModelForm = self.get_form(request, None)

        if request.method == 'POST':
            form = ModelForm(request.POST, request.FILES, instance=None)
            if form.is_valid():
                form_validated = True
                new_object = self.save_form(request, form, change=False)
            else:
                form_validated = False
                new_object = form.instance

            formsets, inline_instances = self._create_formsets(request, new_object)
            if all_valid(formsets) and form_validated:
                self.save_model(request, new_object, form, False)

            self.log_addition(request, new_object)
            return self.response_add(request, new_object, post_url_continue='/management/login/')
        else:
            initial = self.get_changeform_initial_data(request)
            form = ModelForm(initial=initial)
            formsets, inline_instances = self._create_formsets(request, self.model())

            adminForm = helpers.AdminForm(form,
                                          list(self.get_fieldsets(request, None)),
                                          self.get_prepopulated_fields(request, None),
                                          self.get_readonly_fields(request, None),
                                          model_admin=self)
            media = self.media + adminForm.media

            inline_formsets = self.get_inline_formsets(request, formsets, inline_instances, None)
            for inline_formset in inline_formsets:
                media = media + inline_formset.media

            context = dict(self.admin_site.each_context(),
                           title=u'注册%s' % force_text(self.model._meta.verbose_name),
                           adminform=adminForm,
                           object_id=None,
                           original=None,
                           is_popup=(IS_POPUP_VAR in request.POST or
                                     IS_POPUP_VAR in request.GET),
                           to_field=None,
                           media=media,
                           # formsets=formsets,
                           inline_admin_formsets=inline_formsets,
                           errors=helpers.AdminErrorList(form, formsets),
                           preserved_filters=self.get_preserved_filters(request))

            context.update(extra_context or {})
            return self.render_change_form(request,
                                           context,
                                           add=True,
                                           change=False,
                                           obj=None,
                                           form_url=form_url)

admin.site.register(Staff, StaffAdmin)
management_site.register(Staff, StaffAdmin)
