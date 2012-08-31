#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import url, patterns, include


urlpatterns = patterns('django.contrib.auth.views',
    # TODO: remove
    url(r'^logout/$', 'logout', name='logout'),
)
