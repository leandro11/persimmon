#coding=utf-8
import os
import sys

from django.contrib.auth.models import User, Group

from member.models import *
from management.models import Staff
from utils.constants import (
    MEMBER_USER_TYPE, StaffType, STAFF_TYPE, MemberUserType, OperatorType,
    OperationType, FileType, TransactionCategory)
from utils.constants import StaffType
from transaction.models import TransactionMetaOperation

#================================================= 验证用户组 =================================================
def group_check(user_id, group_name):
    '''
    check user's group, return bool
    '''
    try:
        group = Group.objects.get(name=group_name)
    except:
        return False

    count = User.groups.through.objects.filter(user_id=user_id, group_id=group.id).count()
    if count < 1:
        return False
    return True


def get_group(user):
    groups = user.groups.all()
    if len(groups):
        return groups[0].name
    else:
        return None


def get_user_profile(user):
    if isinstance(user, int):
        user = User.objects.get(id=user)

    groups = user.groups.all()
    try:
        if len(groups) > 0:
            if groups[0].id == MemberUserType.BANK_CONTACTOR:
                return BankContactor.objects.get(user=user)
            elif groups[0].id == MemberUserType.BANK_OPERATOR:
                return BankOperator.objects.get(user=user)
            elif groups[0].id == MemberUserType.ENTERPRISE_CONTACTOR:
                return EnterpriseContactor.objects.get(user=user)
            elif groups[0].id == MemberUserType.ENTERPRISE_OPERATOR:
                return EnterpriseOperator.objects.get(user=user)
            elif groups[0].id in StaffType.values:
                return Staff.objects.get(user=user)
        else:
            return None
    except:
        return None


def is_staff_user(user):
    if isinstance(user, int):
        user = User.objects.get(id=user)

    groups = user.groups.all()
    try:
        return groups[0].id in StaffType.values
    except:
        return False


def is_member_user(user):
    if isinstance(user, int):
        user = User.objects.get(id=user)

    groups = user.groups.all()
    try:
        return groups[0].id in MemberUserType.values
    except:
        return False


def create_meta_operation():
    mm = TransactionMetaOperation.objects.filter(
        transaction_type_id=TransactionCategory.TRANSACTION_TYPE3)
    [t.delete() for t in mm]

    op1 = TransactionMetaOperation(
        sequence=1,
        operation_type=OperationType.OPERATION_UPLOAD,
        operator_member=OperatorType.OPERATOR_RECEIVER,
        description=u'传真并上传执行协议',
        need_upload=True,
        need_ems=False,
        need_confirm=True,
        file_name=None,
        transaction_type_id=TransactionCategory.TRANSACTION_TYPE3,
    )
    op2 = TransactionMetaOperation(
        sequence=2,
        operation_type=OperationType.OPERATION_UPLOAD,
        operator_member=OperatorType.OPERATOR_RECEIVER,
        description=u'传真并上传委托声明',
        need_upload=True,
        need_ems=False,
        need_confirm=True,
        file_name=None,
        transaction_type_id=TransactionCategory.TRANSACTION_TYPE3,
    )
    op3 = TransactionMetaOperation(
        sequence=3,
        operation_type=OperationType.OPERATION_CONFIRM,
        operator_member=OperatorType.OPERATOR_PAYER,
        description=u'确认持票人委托声明',
        need_upload=False,
        need_ems=False,
        need_confirm=True,
        file_name=None,
        transaction_type_id=TransactionCategory.TRANSACTION_TYPE3,
    )
    op4 = TransactionMetaOperation(
        sequence=4,
        operation_type=OperationType.OPERATION_EMS,
        operator_member=OperatorType.OPERATOR_PAYER,
        description=u'邮寄汇票至怡智融通',
        need_upload=False,
        need_ems=True,
        need_confirm=False,
        file_name=None,
        transaction_type_id=TransactionCategory.TRANSACTION_TYPE3,
    )
    op5 = TransactionMetaOperation(
        sequence=5,
        operation_type=OperationType.OPERATION_EMS,
        operator_member=OperatorType.OPERATOR_PLATFORM,
        description=u'邮寄汇票至贴现银行',
        need_upload=False,
        need_ems=True,
        need_confirm=True,
        file_name=None,
        transaction_type_id=TransactionCategory.TRANSACTION_TYPE3,
    )
    op6 = TransactionMetaOperation(
        sequence=6,
        operation_type=OperationType.OPERATION_CONFIRM,
        operator_member=OperatorType.OPERATOR_ACCEPTBANK,
        description=u'确认',
        need_upload=False,
        need_ems=False,
        need_confirm=True,
        file_name=None,
        transaction_type_id=TransactionCategory.TRANSACTION_TYPE3,
    )
    op7 = TransactionMetaOperation(
        sequence=7,
        operation_type=OperationType.OPERATION_CONFIRM,
        operator_member=OperatorType.OPERATOR_TICKETBANK,
        description=u'确认收款',
        need_upload=False,
        need_ems=False,
        need_confirm=True,
        file_name=None,
        transaction_type_id=TransactionCategory.TRANSACTION_TYPE3,
    )
    op1.save()
    op2.save()
    op3.save()
    op4.save()
    op5.save()
    op6.save()
    op7.save()


if __name__ == '__main__':
    print 'hello'
    create_meta_operation()