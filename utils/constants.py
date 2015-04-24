# coding=utf-8
import django
import re

class Enum(object):
    def __init__(self, all):
        """
            'all' is either a dict that looks like this:
            {'MEMBER_NAME_1': (1, "Member description 1", ...),
             'MEMBER_NAME_2': (2, "Member description 2", ...), ...}
            or a list that looks like this:
            [(1, "Member 1", ...),
             (2, "Member 2", ...), ...]
        """
        if isinstance(all, dict):
            self.all = all.copy()
        else:
            name = lambda desc: re.sub(
                "[^A-Z0-9_]", "X", re.sub(" ", "_", desc.upper()))
            self.all = dict((name(e[1]), e) for e in all)
        self.all_by_value = dict((i[1][0], (i[0],) + i[1][1:])
                                 for i in self.all.items())
        self.all_by_description = dict((i[1][1], (i[1][0],) + (i[0],))
                                       for i in self.all.items())

    def __repr__(self):
        return '<Enum %s>' % ','.join(self.items)

    __repr__ = __repr__
    __unicode__ = __repr__

    def __getattr__(self, name):
        return self.all[name][0]

    def __dir__(self):
        return self.all.keys()

    def __call__(self, value):
        value = int(value)
        if value not in self.values:
            raise ValueError()
        return value

    @property
    def choices(self):
        return sorted([v[0:2] for v in self.all.values()], key=lambda c: c[0])

    @property
    def items(self):
        return self.all.keys()

    @property
    def values(self):
        return self.all_by_value.keys()

    def get_description(self, value):
        return self.all_by_value[value][1]

    def get_extra(self, value):
        return self.all_by_value[value][2:]

    def get_name(self, value):
        return self.all_by_value[value][0]

    def append(self, enum_with_new_values):
        """
        Update the values in `self` with the values in enum_with_new_values,
        returns a new Enum.
        """
        new_dict = self.all.copy()
        new_dict.update(enum_with_new_values.all)
        return Enum(new_dict)

    def get_by_description(self, description):
        """
        Get the enum by its descriptional value.
        :param str description The enum description.
        :rtype: Enum|None
        :return The enum or None when no enum exists with that name.
        """
        descriptions = self.all_by_description
        if description not in descriptions:
            return None
        else:
            return descriptions[description][0]

#================================================ 管理员的角色列表 =============================================

StaffType = Enum({
    'MARKET_MANAGER': (5, u"市场部总经理"),
    'ZONE_MARKET': (6, u"区域市场经理"),
    'SERVICE_MANAGER': (7, u"客服部总经理"),
    'ZONE_SERVICE': (8, u"区域客服"),
    'TICKET_CONDUCTOR': (9, u"核票员"),
    'TICKET_DIRECTOR': (10, u"票据主管"),
    'ACCOUNTANT': (11, u"会计"),
    'TOP_MANAGER': (12, u"总经理"),
})

STAFF_TYPE = [(item[1], item[1]) for item in StaffType.choices]

#================================================ 用户角色名称 =============================================

MemberType = Enum({
    'MEMBER_BANK': (1, u'银行会员'),
    'MEMBER_ENTERPRISE': (2, u'企业会员'),
    'MEMBER_PLATFORM': (3, u'怡智融通'),
})

MemberUserType = Enum({
    'BANK_CONTACTOR': (1, u'银行会员主联络人'),
    'BANK_OPERATOR': (2, u'银行会员执行人'),
    'ENTERPRISE_CONTACTOR': (3, u'企业会员主联络人'),
    'ENTERPRISE_OPERATOR': (4, u'企业会员执行人'),
})

MEMBER_USER_TYPE = [(item[1], item[1]) for item in MemberType.choices]
#=============================================================================================

MEMBER_BANK = u'BANK'
MEMBER_ENTERPRISE = u'ENTERPRISE'
MEMBER_PLATFORM = u'PLATFORM'

MEMBER_TYPE = (
    (MEMBER_BANK, '银行会员'),
    (MEMBER_ENTERPRISE, '企业会员'),
    (MEMBER_PLATFORM, '怡智融通'),
)

# BANK_CONTACTOR = u'银行会员主联络人'
# BANK_OPERATOR = u'银行会员执行人'
# ENTERPRISE_CONTACTOR = u'企业会员主联络人'
# ENTERPRISE_OPERATOR = u'企业会员执行人'

# MEMBER_USER_TYPE = (
#     (BANK_CONTACTOR, BANK_CONTACTOR),
#     (BANK_OPERATOR, BANK_OPERATOR),
#     (ENTERPRISE_CONTACTOR, ENTERPRISE_CONTACTOR),
#     (ENTERPRISE_OPERATOR, ENTERPRISE_OPERATOR),
# )

# ======================================= 发票状态 =======================================
INVOICE_UNLODGED = 'UNLODGED'
# INVOICE_LODGED = 'LODGED'
INVOICE_LODGED = 'LODGED'
INVOICE_PENDING = 'PENDING'
INVOICE_FINISHED = 'FINISHED'
INVOICE_ABORT = 'ABORT'

# for invoice model
INVOICE_STATUS = (
    # (INVOICE_UNLODGED, u'未开具'),
    # (INVOICE_LODGED, u'已申请'),
    (INVOICE_LODGED, u'已开具'),
    # (INVOICE_PENDING, u'待审核'),
    (INVOICE_FINISHED, u'已寄出'),
    # (INVOICE_ABORT, u'已作废'),
)

# for transaction order model
INVOICE_STATUS2 = (
    (INVOICE_UNLODGED, u'未开具'),
    # (INVOICE_LODGED, u'已申请'),
    (INVOICE_LODGED, u'已开具'),
    # (INVOICE_PENDING, u'待审核'),
    (INVOICE_FINISHED, u'已寄出'),
    # (INVOICE_ABORT, u'已作废'),
)

# ======================================= 汇票状态 =======================================

TICKET_RECEIVED = 'RECEIVED'
TICKET_VERIFIED = 'VERIFIED'
TICKET_CHECKIN = 'CHECKIN'
TICKET_CHECKOUT = 'CHECKOUT'
TICKET_ABORT = 'ABORT'
TICKET_RECEIVED_PENDING = 'RECEIVED_PENDING'
TICKET_VERIFIED_PENDING = 'VERIFIED_PENDING'
TICKET_CHECKIN_PENDING = 'CHECKIN_PENDING'
TICKET_CHECKOUT_PENDING = 'CHECKOUT_PENDING'
TICKET_ABORT_PENDING = 'ABOR_PENDINGT'
TICKET_UNRECEIVED = 'UNRECEIVED'

# for tansaction ticket model
TICKET_STATUS = (
    # (TICKET_UNRECEIVED, u'未开始'),
    (TICKET_RECEIVED_PENDING, u'收票待核'),
    (TICKET_RECEIVED, u'收票完成'),
    (TICKET_VERIFIED_PENDING, u'验票待核'),
    (TICKET_VERIFIED, u'验票完成'),
    (TICKET_CHECKIN_PENDING, u'入库待核'),
    (TICKET_CHECKIN, u'入库完成'),
    (TICKET_CHECKOUT_PENDING, u'出库待核'),
    (TICKET_CHECKOUT, u'出库完成'),
)

# for tansaction order model
TICKET_STATUS2 = (
    (TICKET_UNRECEIVED, u'未收票'),
    (TICKET_RECEIVED_PENDING, u'收票待核'),
    (TICKET_RECEIVED, u'收票已核'),
    (TICKET_VERIFIED_PENDING, u'验票待核'),
    (TICKET_VERIFIED, u'验票已核'),
    (TICKET_CHECKIN_PENDING, u'入库待核'),
    (TICKET_CHECKIN, u'入库已核'),
    (TICKET_CHECKOUT_PENDING, u'出库待核'),
    (TICKET_CHECKOUT, u'出库已核'),
    # (TICKET_ABORT_PENDING, u'作废待核'),
    # (TICKET_ABORT, u'作废已核'),
)


