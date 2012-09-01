#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import url, patterns
from django.views.generic import TemplateView


urlpatterns = patterns('',
    url(r'^/$', TemplateView.as_view(template_name="core/home.html"),
        name='home'),
)
