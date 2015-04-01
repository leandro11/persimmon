#coding=utf-8

from django.shortcuts import render
from django.http import HttpResponse
from django.utils.http import urlquote, urlunquote
from utils.func import *
from django.http import Http404, HttpResponseRedirect
from django.core.exceptions import PermissionDenied
from TTMS.settings import MEDIA_URL
from utils.models import *
from django.views.decorators.csrf import csrf_protect


def get_template_document(request, filename):
    if not request.user.is_authenticated():
        raise PermissionDenied
    if filename:
        name = urlunquote(filename)
        attachment = TemplateAttachment.objects.get(name=name)
        filename = attachment.file.path
        return show_file(filename)

    return Http404


def get_template_thumbnail(request, filename):
    if not request.user.is_authenticated():
        raise PermissionDenied
    if filename:
        name = urlunquote(filename)
        attachment = TemplateAttachment.objects.get(name=name)
        if attachment.thumbnail:
            filename = attachment.thumbnail.path
            return show_file(filename)

    return Http404


def send_sms_verify(request):
    if request.method == 'POST':
        return HttpResponse('{"result":true}')
    return HttpResponse('{"result":true}')


def send_email_verify(request):
    return HttpResponse('true')
