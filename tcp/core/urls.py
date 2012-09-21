#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import url, patterns

from .views import create_view, detail_view, validate

urlpatterns = patterns('',
    url(r'^$', create_view, name='home'),
    url(r'^validate/(?P<provider>[^/]+)/(?P<video_id>[^/]+)$', validate,
        name='validate'),
    url(r'^(?P<pk>[^/]+)$', detail_view, name='cleaned'),
)
