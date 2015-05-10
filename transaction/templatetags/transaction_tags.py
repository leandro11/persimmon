#coding=utf-8

from django import template

from utils.user import group_check, get_group, get_user_profile
from transaction.models import *
from utils.constants import OperationStatus, OperatorType

register = template.Library()


def cut(value, arg):
    """Removes all values of arg from the given string"""
    return value.replace(arg, '')


register.filter('cut', cut)


def lower(value):  # Only one argument.
    """Converts a string into all lowercase"""
    return value.lower()


register.filter('lower', lower)


def get_profile_name(user):
    user_profile = get_user_profile(user)
    if user_profile:
        # return '[%s]%s' % (user_profile.groupname, user_profile.name)
        return user_profile.name
    else:
        return ''


register.filter('get_profile_name', get_profile_name)


def get_group_name(user):
    user_profile = get_user_profile(user)
    if user_profile:
        # return '[%s]%s' % (user_profile.groupname, user_profile.name)
        return user_profile.groupname
    else:
        return ''


register.filter('get_group_name', get_group_name)


def get_operator_user_link(operation):
    user = operation.operator_user
    user_profile = get_user_profile(user)
    if user_profile:
        group_name = None if user_profile is None else user_profile.groupname
        tagid = 'op%s_%s_%s' % (operation.id, user_profile._meta.object_name.lower(), user_profile.id)
        telephone = user_profile.telephone if user_profile.telephone else ''
        return u'''<a href="#%s" onclick="ShowTips('%s');return false;" title="点击查看个人信息"><img src="/static/style/img/icon_info.png"><b>%s</b></a>
                    <div unselectable="on" id="%s" class="tipscontent" style="display: none">
                        <b>%s</b><a style="float:right" href="#" onclick="ShowTips('%s');return false;">[关闭窗口]</a><br/>
                        角色：%s<br/>
                        手机：%s<br/>
                        电话：%s<br/>
                    </div>''' \
               % (tagid, tagid, user_profile.name, tagid, user_profile.name, tagid, group_name, user_profile.mobile_number, telephone)
    else:
        return 'error_no_profile'


register.filter('get_operator_user_link', get_operator_user_link)


def get_processing_operation(order):
    res = u''
    operation_list = TransactionOperation.objects.filter(transaction=order).order_by('sequence').all()
    for op in operation_list:
        if op.status in [OperationStatus.OPERATION_ACTIVATED, OperationStatus.OPERATION_PENDING]:
            if op.operator_member == OperatorType.OPERATOR_RECEIVER:
                member_name = Enterprise.objects.get(id=op.transaction.receivable_enterprise_id).name
            elif op.operator_member == OperatorType.OPERATOR_PAYER:
                member_name = Enterprise.objects.get(id=op.transaction.pay_enterprise_id).name
            elif op.operator_member == OperatorType.OPERATOR_TICKETBANK:
                member_name = Bank.objects.get(id=op.transaction.ticket_bank_id).short_name
            elif op.operator_member == OperatorType.OPERATOR_ACCEPTBANK:
                member_name = Bank.objects.get(id=op.transaction.accept_bank_id).short_name
            else:
                member_name = u'怡智融通'

            res += u'<td></td><td colspan="10">当前进度：%s %s %s</td>' % (member_name, op.description, op.get_status_display())

    return '<tr class="row1">' + res + '</tr>'


register.filter('get_processing_operation', get_processing_operation)


def show_operation_attachment(file):
    base, ext = os.path.splitext(os.path.basename(file.path))
    ext = ext.lower()
    # filename = '%s_thumb%s' % (base, ext)
    if ext == '.jpg' or ext == '.png' or ext == '.gif' or ext == '.jpeg':
        return u'<p><a href="%s"><img width="100px" src="%s" /><br/><b>查看附件</b></a></p>' % (file.url, file.url)
    else:
        return u'<p><a href="%s"><img width="100px" src="/static/style/img/doc.png" /><br/><b>查看附件</b></a></p>' % file.url


register.filter('show_operation_attachment', show_operation_attachment)
