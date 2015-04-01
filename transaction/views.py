#coding=utf-8
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from utils.func import *
from transaction.models import *
from django.http import Http404, HttpResponseRedirect
from django.core.exceptions import PermissionDenied


def get_operation_attachment(request, transaction_id, operation_id, filename):
    if not request.user.is_authenticated():
        raise PermissionDenied
    # todo permission check
    if operation_id.isdigit() and transaction_id.isdigit():
        operation = TransactionOperation.objects.get(pk=long(operation_id))
        if operation.transaction_id == long(transaction_id) and operation.upload_file_name == filename:
            return show_file(operation.upload_file.path)
    return Http404


def get_operation_attachment_thumbnail(request, transaction_id, operation_id, filename):
    if not request.user.is_authenticated():
        raise PermissionDenied
    # todo permission check
    if operation_id.isdigit() and transaction_id.isdigit():
        operation = TransactionOperation.objects.get(pk=long(operation_id))
        if operation.transaction_id == long(transaction_id) and operation.upload_file_name == filename:
            return show_file(operation.upload_file_thumbnail.path)
    return Http404
