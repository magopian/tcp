#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ratelimitbackend import admin

from .models import Request


class RequestAdmin(admin.ModelAdmin):
    list_display = ('video_link', 'is_valid', 'provider')
    list_filter = ('is_valid', 'provider')
    model = Request
    ordering = ['-id']
    search_fields = ('initial_code',)


admin.site.register(Request, RequestAdmin)
