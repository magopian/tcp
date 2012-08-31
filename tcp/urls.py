#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf import settings
from django.conf.urls import url, patterns, include
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.http import HttpResponse, HttpResponsePermanentRedirect

from ratelimitbackend import admin
from ratelimitbackend.forms import AuthenticationForm
from raven.contrib.django.models import client

admin.autodiscover()

client.captureException()


robots = lambda _: HttpResponse('User-agent: *\nDisallow:\n',
                                mimetype='text/plain')

humans = lambda _: HttpResponse(u"""/* TEAM */
Main developer: Mathieu Agopian
Contact: mathieu.agopian [at] gmail.com
Twitter: @magopian
From: France

/* SITE */
Language: English
Backend: Django, PostgreSQL
Frontend: SCSS, Compass
""", mimetype='text/plain; charset=UTF-8')

favicon = lambda _: HttpResponsePermanentRedirect(
    '%score/img/icon-tcp.png' % settings.STATIC_URL
)

touch_icon = lambda _: HttpResponsePermanentRedirect(
    '%score/img/touch-icon-114.png' % settings.STATIC_URL
)

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
    url(r'^robots.txt$', robots),
    url(r'^humans.txt$', humans),
    url(r'^favicon.ico$', favicon),
    url(r'^apple-touch-icon-precomposed.png$', touch_icon),
    (r'^', include('tcp.core.urls', namespace='core')),
)

urlpatterns += patterns('ratelimitbackend.views',
    url(r'^login/$', 'login',
        {'authentication_form': AuthenticationForm}, name='login'),
)

urlpatterns += patterns('django.contrib.auth.views',
    url(r'^logout/$', 'logout', name='logout'),
)

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
