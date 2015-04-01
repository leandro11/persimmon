#coding=utf-8
# -*- coding: utf-8 -*-\

from django.contrib import admin
from utils.models import *
from utils.form import TemplateAttachmentChangeForm
from django.forms import ModelForm
from django.db import transaction
from management.sites import site as management_site


class TemplateAttachmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'type', 'get_link', 'get_thumbnail_link']

    @transaction.atomic
    def add_view(self, request, form_url='', extra_context=None):
        self.exclude = ['name', 'extension', 'size', 'width', 'height', 'thumbnail', 'creator']
        self.readonly_fields = []
        self.form = ModelForm

        if request.user.is_superuser:
            pass

        return super(TemplateAttachmentAdmin, self).add_view(request, form_url, extra_context)

    @transaction.atomic
    def change_view(self, request, object_id, form_url='', extra_context=None):
        self.exclude = []
        self.readonly_fields = ['name', 'extension', 'size', 'width', 'height', 'thumbnail']
        self.form = TemplateAttachmentChangeForm
        return super(TemplateAttachmentAdmin, self).change_view(request, object_id, form_url, extra_context)

    @transaction.atomic
    def save_model(self, request, obj, form, change):
        if request.method == 'POST' and 'file' in request.FILES:
            obj.creator = request.user

        super(TemplateAttachmentAdmin, self).save_model(request, obj, form, change)


management_site.register(TemplateAttachment, TemplateAttachmentAdmin)

admin.site.register(TemplateAttachment, TemplateAttachmentAdmin)