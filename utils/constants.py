#coding=utf-8

import django

#================================================ 用户角色名称 =============================================

MEMBER_BANK = u'BANK'
MEMBER_ENTERPRISE = u'ENTERPRISE'
MEMBER_PLATFORM = u'PLATFORM'

MEMBER_TYPE = (
    (MEMBER_BANK, '银行会员'),
    (MEMBER_ENTERPRISE, '企业会员'),
    (MEMBER_PLATFORM, '怡智融通'),
)

BANK_CONTACTOR = u'银行会员主联络人'
BANK_OPERATOR = u'银行会员执行人'
ENTERPRISE_CONTACTOR = u'企业会员主联络人'
ENTERPRISE_OPERATOR = u'企业会员执行人'

MEMBER_USER_TYPE = (
    (BANK_CONTACTOR, BANK_CONTACTOR),
    (BANK_OPERATOR, BANK_OPERATOR),
    (ENTERPRISE_CONTACTOR, ENTERPRISE_CONTACTOR),
    (ENTERPRISE_OPERATOR, ENTERPRISE_OPERATOR),
)
# todo @zhangnan django的group里必须新建以这些名称作为name的group记录
MARKET_MANAGER = u'市场部总经理'
ZONE_MARKET = u'区域市场经理'
SERVICE_MANAGER = u'客服部总经理'
ZONE_SERVICE = u'区域客服'
TOP_MANAGER = u'总经理'    # is_superuser == True
TICKET_CONDUCTOR = u'核票员'
TICKET_DIRECTOR = u'票据主管'
ACCOUNTANT = u'会计'

STAFF_TYPE = (
    (MARKET_MANAGER, MARKET_MANAGER),
    (ZONE_MARKET, ZONE_MARKET),
    (SERVICE_MANAGER, SERVICE_MANAGER),
    (ZONE_SERVICE, ZONE_SERVICE),
    (TOP_MANAGER, TOP_MANAGER),
    (TICKET_CONDUCTOR, TICKET_CONDUCTOR),
    (TICKET_DIRECTOR, TICKET_DIRECTOR),
    (ACCOUNTANT, ACCOUNTANT),
)

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


