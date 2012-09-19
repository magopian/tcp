#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ratelimitbackend import admin

from .models import Request


class RequestAdmin(admin.ModelAdmin):
    list_display = ('video_id', 'provider')
    list_filter = ('provider',)
    ordering = ('-id',)
    search_fields = ('initial_code',)


admin.site.register(Request, RequestAdmin)
