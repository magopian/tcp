#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.test import TestCase

from tcp.provider.models import Provider, LinkMatch

from .models import Request


class RequestTest(TestCase):
    """Test the request"""

    def test_match_provider(self):
        """Match a provider from a video embed code"""
        provider = Provider.objects.create(name='Foo',
                                           link_template='bar',
                                           embed_template='baz')
        match = LinkMatch.objects.create(provider=provider,
                                         pattern='foo_video')
        # matching request
        request = Request.objects.create(initial_code='some stuff foo_video')
        self.assertTrue(request.match())
        self.assertEqual(request.provider, provider)
        # non matching request
        request = Request.objects.create(initial_code='some stuff foo video')
        self.assertFalse(request.match())
