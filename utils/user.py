#coding=utf-8

from member.models import *
from django.contrib.auth.models import User, Group
from utils.constants import (BANK_CONTACTOR, BANK_OPERATOR, ENTERPRISE_CONTACTOR,
    ENTERPRISE_OPERATOR, MEMBER_USER_TYPE, StaffType, STAFF_TYPE)
from management.models import Staff
from utils.constants import StaffType

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
    # if not user.is_authenticated():
    #     return HttpResponseRedirect('/member/login')

    groups = user.groups.all()
    try:
        if len(groups) > 0:
            if groups[0].name == BANK_CONTACTOR:
                return BankContactor.objects.get(user=user)
            elif groups[0].name == BANK_OPERATOR:
                return BankOperator.objects.get(user=user)
            elif groups[0].name == ENTERPRISE_CONTACTOR:
                return EnterpriseContactor.objects.get(user=user)
            elif groups[0].name == ENTERPRISE_OPERATOR:
                return EnterpriseOperator.objects.get(user=user)
            elif groups[0].id in StaffType.values:
                return Staff.objects.get(user=user)
        else:
            return None
    except:
        return None




