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
                                           link_template='_',
                                           embed_template='_')
        match = LinkMatch.objects.create(provider=provider,
                                         pattern='foo_video')
        # matching request
        request = Request.objects.create(initial_code='some stuff foo_video')
        res, prov = request.match()
        self.assertTrue(res)
        self.assertEqual(prov, provider)
        # matching request ignore case
        request = Request.objects.create(initial_code='some stuff FOO_VIDEO')
        res, prov = request.match()
        self.assertTrue(res)
        self.assertEqual(prov, provider)
        # matching request multiline
        request = Request.objects.create(initial_code='some stuff\nFOO_VIDEO')
        res, prov = request.match()
        self.assertTrue(res)
        self.assertEqual(prov, provider)
        # non matching request
        request = Request.objects.create(initial_code='some stuff foo video')
        res = request.match()
        self.assertFalse(res)

    def test_get_link(self):
        """Compute a full video link from a video id"""
        provider = Provider.objects.create(
                name='Foo',
                link_template='http://{{ video_id }}',
                embed_template='_')
        match = LinkMatch.objects.create(provider=provider,
                                         pattern='foo_video/(?P<id>.*)')
        # matching request
        request = Request.objects.create(initial_code='stuff foo_video/barbaz')
        link = request.get_link('barbaz', provider)
        self.assertEqual(link, 'http://barbaz')
