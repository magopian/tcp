#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ratelimitbackend import admin

from .models import Provider, LinkMatch


class LinkMatchInline(admin.TabularInline):
    model = LinkMatch

class ProviderAdmin(admin.ModelAdmin):
    inlines = [LinkMatchInline]
    model = Provider
    ordering = ['name']
    search_fields = ('name',)


admin.site.register(Provider, ProviderAdmin)
