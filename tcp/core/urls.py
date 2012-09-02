#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import url, patterns

from .views import create_view, detail_view

urlpatterns = patterns('',
    url(r'^$', create_view, name='home'),
    url(r'^(?P<pk>[^/]+)$', detail_view, name='cleaned'),
)
