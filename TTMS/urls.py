#coding=utf-8
from django.conf.urls import patterns, include, url
from django.contrib.auth.views import (
    password_reset, password_reset_done, password_reset_confirm,
    password_reset_complete, password_change, password_change_done)
from django.contrib import admin
from TTMS.site import site as admin_site
from member.sites import site as member_site
from management.sites import site as management_site


urlpatterns = patterns(
    '',
    #=================================== ADMIN =================================
    # url(r'^admin/$', admin.site.index, name='index'),
    # url(r'^admin/login/$', admin.site.login, name='login'),
    # url(r'^admin/logout/$', admin.site.logout, name='logout'),
    # url(r'^admin/password_change/$', admin.site.password_change, name='password_change'),
    # url(r'^admin/password_change/done/$', admin.site.password_change_done, name='password_change_done'),
    # url(r'^admin/jsi18n/$', admin.site.i18n_javascript, name='jsi18n'),
    # url(r'^admin/r/(?P<content_type_id>\d+)/(?P<object_id>.+)/$', contenttype_views.shortcut, name='view_on_site'),

    url(r'^', include(member_site.urls)),
    url(r'^staff/', include(management_site.urls)),
    url(r'^admin/', include(admin.site.urls)),

    # #=================================== BANK ===============================
    # url(r'^member/bank_register/$', 'member.views.bank_register'),
    # url(r'^member/bank_login/$', 'member.views.bank_login'),
    # url(r'^member/create_bank/$', 'member.views.create_bank'),
    # # url(r'^member/createbank/$', BankCreateView.as_view(), name='createbank'),
    # #=================================== ENTERPRISE ===============================
    # url(r'^member/enterprise_register/$', 'member.views.enterprise_register'),
    # url(r'^member/enterprise_login/$', 'member.views.enterprise_login'),

    # 登陆后根据用户身份统一跳转
    url(r'^login_redirect/$', 'TTMS.auth.login_redirect'),

    #=================================== MANAGEMENT ===============================
    url(r'^management/login/$', 'management.auth.login'),
    url(r'^management/logout/$', 'management.auth.logout'),
    url(r'^management/logout_then_login/$', 'management.auth.logout_then_login'),
    url(r'^management/redirect_to_login/$', 'management.auth.redirect_to_login'),
    # password
    url(r'^management/password_reset/$', password_reset, {'post_reset_redirect': '/management/password_reset_done'}),
    url(r'^management/password_reset_done/$', password_reset_done),
    url(r'^management/password_reset_confirm/$', password_reset_confirm),
    url(r'^management/password_reset_complete/$', password_reset_complete),
    # password_change
    url(r'^management/password_change/$', password_change, {'post_change_redirect': '/management/password_change_done'}),
    url(r'^management/password_change_done/$', password_change_done, {'template_name': 'registration/password_change_done.html'}),
    # 工作人员dashboard主界面
    url(r'^management/main/$', 'management.views.main_view'),

    #=================================== MEMBER ===============================
    url(r'^member/login/', 'member.auth.login'),
    url(r'^member/logout/', 'member.auth.logout'),
    url(r'^member/logout_then_login/', 'member.auth.logout_then_login'),
    url(r'^member/redirect_to_login/', 'member.auth.redirect_to_login'),
    # password_reset
    # todo reset 除了邮箱还要加上手机
    url(r'^member/password_reset/$', password_reset, {'template_name': 'member/registration/password_reset_form.html', 'post_reset_redirect': '/member/password_reset_done'}),
    url(r'^member/password_reset_done/$', password_reset_done, {'template_name': 'member/registration/password_reset_done.html'}),
    url(r'^member/password_reset_confirm/$', password_reset_confirm, {'template_name': 'member/registration/password_reset_confirm.html'}),
    url(r'^member/password_reset_complete/$', password_reset_complete, {'template_name': 'member/registration/password_reset_complete.html'}),

    # password_change
    # moved into member/sites.py
    # url(r'^member/password_change/$', password_change, {'post_change_redirect': '/member/password_change_done'}),
    # url(r'^member/password_change_done/$', password_change_done, {'template_name': 'registration/password_change_done.html'}),

    # 主界面
    url(r'^member/main/$', 'member.views.member_main'),

    # 附件
    url(r'^template/thumbnail/(?P<filename>.*)$', 'utils.views.get_template_thumbnail'),
    url(r'^template/(?P<filename>.*)$', 'utils.views.get_template_document'),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': './media', 'show_indexes': True}),
    url(r'^bank/(?P<bank_id>.*)/attachment/thumbnail/(?P<filename>.*)$', 'member.views.get_bank_attachment_thumbnail'),
    url(r'^bank/(?P<bank_id>.*)/attachment/(?P<filename>.*)$', 'member.views.get_bank_attachment'),
    url(r'^enterprise/(?P<enterprise_id>.*)/attachment/thumbnail/(?P<filename>.*)$', 'member.views.get_enterprise_attachment_thumbnail'),
    url(r'^enterprise/(?P<enterprise_id>.*)/attachment/(?P<filename>.*)$', 'member.views.get_enterprise_attachment'),
    url(r'^transactionorder/(?P<transaction_id>.*)/operation/(?P<operation_id>.*)/attachment/thumbnail/(?P<filename>.*)$', 'transaction.views.get_operation_attachment_thumbnail'),
    url(r'^transactionorder/(?P<transaction_id>.*)/operation/(?P<operation_id>.*)/attachment/(?P<filename>.*)$', 'transaction.views.get_operation_attachment'),

    # 手机邮件验证码
    url(r'^send_sms_verify.php', 'utils.views.send_sms_verify'),
    url(r'^utils/send_sms_verify', 'utils.views.send_sms_verify'),
    url(r'^utils/send_email_verify/$', 'utils.views.send_email_verify'),

)













