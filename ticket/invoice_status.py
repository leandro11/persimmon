#coding=utf-8

from utils.constants import InvoiceStatus


class InvoiceState(object):
    """
    Basic Invoice State
    """

    def __init__(self, invoice_obj):
        """
        :param request: Invoice Object
        """
        self.invoice_obj = invoice_obj

    def show_link(self, **kwargs):
        raise NotImplementedError()

    def send(self, **kwargs):
        raise NotImplementedError()


class UnlodgedState(InvoiceState):

    def __init__(self, invoice_obj):
        super(UnlodgedState, self).__init__(invoice_obj)

    def show_link(self, **kwargs):
        return u''

    def send(self, **kwargs):
        pass


class LodgedState(InvoiceState):

    def __init__(self, invoice_obj):
        super(LodgedState, self).__init__(invoice_obj)

    def show_link(self, **kwargs):
        return u'<a class="button" href="/staff/ticket/invoice/%s/send"><strong>发票寄出</strong></a>' % self.invoice_obj.id

    def send(self, **kwargs):
        # Change current invoice_obj's status
        self.invoice_obj.status = InvoiceStatus.INVOICE_FINISHED

        # Change transaction invoice status
        self.invoice_obj.transaction.invoice_status = InvoiceStatus.INVOICE_FINISHED


class FinishedState(InvoiceState):

    def __init__(self, invoice_obj):
        super(FinishedState, self).__init__(invoice_obj)

    def show_link(self, **kwargs):
        return u'已寄出'

    def send(self, **kwargs):
        pass


class AbortState(InvoiceState):

    def __init__(self, invoice_obj):
        super(AbortState, self).__init__(invoice_obj)

    def show_link(self, **kwargs):
        return u'已作废'

    def send(self, **kwargs):
        pass
