#coding=utf-8

import django
from django.contrib import admin
from django.conf import settings
from functools import update_wrapper
from django.utils import six
from django.core.exceptions import PermissionDenied, ValidationError

from management import auth
from management.views import register
from management.views import main_view
from utils.user import group_check, get_group, get_user_profile
from management.models import *


class ManagementAdminSite(admin.AdminSite):
    def get_urls(self):
        from django.conf.urls import patterns, url, include
        # Since this module gets imported in the application's root package,
        # it cannot import models from other applications at the module level,
        # and django.contrib.contenttypes.views imports ContentType.
        from django.contrib.contenttypes import views as contenttype_views

        if settings.DEBUG:
            self.check_dependencies()

        def wrap(view, cacheable=False):
            def wrapper(*args, **kwargs):
                return self.admin_view(view, cacheable)(*args, **kwargs)

            return update_wrapper(wrapper, view)

        # Admin-site-wide views.
        urlpatterns = patterns('',
                               url(r'^management/main$', main_view, name='management_index'),
                               url(r'^management/login/$', auth.login, name='management_login'),
                               url(r'^management/logout/$', auth.logout, name='management_logout'),
                               url(r'^management/password_change/$', django.contrib.auth.views.password_change,
                                   {'post_change_redirect': '/management/password_change_done', 'template_name': 'management/registration/password_change_form.html'},
                                   name='management_password_change'),
                               url(r'^management/password_change_done/$', django.contrib.auth.views.password_change_done,
                                   {'template_name': 'management/registration/password_change_done.html'},
                                   name='password_change_done'),
                               url(r'^management/jsi18n/$', wrap(self.i18n_javascript, cacheable=True), name='jsi18n'),
                               url(r'^management/r/(?P<content_type_id>\d+)/(?P<object_id>.+)/$', wrap(contenttype_views.shortcut), name='view_on_site'),
        )

        # Add in each model's views, and create a list of valid URLS for the
        # app_index
        valid_app_labels = []
        for model, model_admin in six.iteritems(self._registry):
            urlpatterns += patterns('',
                                    url(r'^%s/%s/' % (model._meta.app_label, model._meta.model_name), include(model_admin.urls))
            )
            if model._meta.app_label not in valid_app_labels:
                valid_app_labels.append(model._meta.app_label)

        # If there were ModelAdmins registered, we should have a list of app
        # labels for which we need to allow access to the app_index view,
        if valid_app_labels:
            regex = r'^(?P<app_label>' + '|'.join(valid_app_labels) + ')/$'
            urlpatterns += patterns('',
                                    url(regex, wrap(self.app_index), name='app_list'),
            )
        return urlpatterns

    def app_index(self, request, app_label, extra_context=None):
        if request.user.is_superuser:
            return super(ManagementAdminSite, self).app_index(request, app_label, extra_context)
        else:
            raise PermissionDenied

    def has_permission(self, request):
        user_profile = get_user_profile(request.user)
        if isinstance(user_profile, Staff):
            return super(ManagementAdminSite, self).has_permission(request)
        else:
            return False


site = ManagementAdminSite(name='management', app_name='management')