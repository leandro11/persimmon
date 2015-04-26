#coding=utf-8

from django.test import RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware


def create_test_request(url, method='get'):
    factory = RequestFactory()
    middleware = SessionMiddleware()

    if method == 'post':
        request = factory.post(url)
    else:
        request = factory.get(url)

    middleware.process_request(request)
    request.session.save()

    return request
