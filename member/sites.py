__author__ = 'Lorne'

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
from utils.constants import StaffType, MemberUserType


class MemberAdminSite(admin.AdminSite):
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
                               url(r'^member/main$', member_main, name='member_index'),
                               url(r'^member/login/$', auth.login, name='member_login'),
                               url(r'^member/logout/$', auth.logout, name='member_logout'),
                               url(r'^member/password_change/$', django.contrib.auth.views.password_change,
                                   {'post_change_redirect': '/member/password_change_done', 'template_name': 'member/registration/password_change_form.html'},
                                   name='member_password_change'),
                               url(r'^member/password_change_done/$', django.contrib.auth.views.password_change_done,
                                   {'template_name': 'member/registration/password_change_done.html'},
                                   name='password_change_done'),
                               url(r'^member/jsi18n/$', wrap(self.i18n_javascript, cacheable=True), name='jsi18n'),
                               url(r'^member/r/(?P<content_type_id>\d+)/(?P<object_id>.+)/$', wrap(contenttype_views.shortcut), name='view_on_site'),
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
            return super(MemberAdminSite, self).app_index(request, app_label, extra_context)
        else:
            raise PermissionDenied

    def has_permission(self, request):
        user_profile = get_user_profile(request.user)
        group_type = None if user_profile is None else user_profile.grouptype

        if group_type in MemberUserType.values:
            return super(MemberAdminSite, self).has_permission(request)
        else:
            return False


site = MemberAdminSite(name='member', app_name='member')

