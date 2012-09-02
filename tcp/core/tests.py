#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client

from tcp.provider.models import Provider, LinkMatch

from .models import Request


class RequestTest(TestCase):
    """Test the request"""

    def test_match_provider(self):
        """Match a provider."""
        provider = Provider.objects.create(name='Foo',
                                           link_template='_',
                                           embed_template='_')
        match = LinkMatch.objects.create(provider=provider,
                                         pattern='foo_video/(.*)')
        # matching request
        request = Request(initial_code='some stuff foo_video/barbaz')
        res, prov = request.match()
        self.assertTrue(res)
        self.assertEqual(prov, provider)
        # matching request ignore case
        request = Request(initial_code='some stuff FOO_VIDEO/barbaz')
        res, prov = request.match()
        self.assertTrue(res)
        self.assertEqual(prov, provider)
        # matching request multiline
        request = Request(initial_code='some stuff\nFOO_VIDEO/barbaz')
        res, prov = request.match()
        self.assertTrue(res)
        self.assertEqual(prov, provider)
        # non matching request
        request = Request(initial_code='some stuff video/barbaz')
        res, prov = request.match()
        self.assertIsNone(res)

    def test_get_link(self):
        """Compute full video link."""
        provider = Provider.objects.create(
                name='Foo',
                link_template='http://{{ video_id }}',
                embed_template='_')
        match = LinkMatch.objects.create(provider=provider,
                                         pattern='foo_video/(.*)')
        request = Request(initial_code='stuff foo_video/barbaz')
        link = request.get_link('barbaz', provider)
        self.assertEqual(link, 'http://barbaz')

    def test_get_clean_code(self):
        """Compute the new embed code."""
        provider = Provider.objects.create(
                name='Foo',
                link_template='_',
                embed_template='some code {{ video_link }}')
        match = LinkMatch.objects.create(provider=provider,
                                         pattern='foo_video/(.*)')
        request = Request(initial_code='stuff foo_video/barbaz')
        link = request.get_clean_code('http://barbaz', provider)
        self.assertEqual(link, 'some code http://barbaz')

    def test_save(self):
        """Process a request"""
        provider = Provider.objects.create(
                name='Foo',
                link_template='http://{{ video_id }}',
                embed_template='some code {{ video_link }}')
        match = LinkMatch.objects.create(provider=provider,
                                         pattern='foo_video/(.*)')
        # matching request
        request = Request(initial_code='stuff foo_video/barbaz')
        request.save()
        self.assertEqual(request.provider, provider)
        self.assertEqual(request.video_link, 'http://barbaz')
        self.assertEqual(request.clean_code, 'some code http://barbaz')
        # non matching request
        request = Request(initial_code='stuff video/barbaz')
        request.save()
        self.assertEqual(request.provider, None)
        self.assertEqual(request.message, 'No provider found for this video')


class RequestViewTest(TestCase):
    """Test the views"""

    def setUp(self):
        self.client = Client()

    def test_create_view(self):
        """Create view"""
        home_url = reverse('core:home')
        self.assertEqual(Request.objects.count(), 0)
        # invalid form post
        with self.assertTemplateUsed('core/home.html'):
            response = self.client.post(home_url, {'initial_code': ''})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Request.objects.count(), 0)
        # proper form post
        with self.assertTemplateUsed('core/home.html'):
            response = self.client.post(home_url, {'initial_code': 'foo'},
                                        follow=True)
        self.assertRedirects(response, home_url)
        self.assertEqual(Request.objects.count(), 1)  # creates a request

    def test_create_view_json(self):
        """Create view, with 'Accept' header set to json"""
        home_url = reverse('core:home')
        self.assertEqual(Request.objects.count(), 0)
        # invalid form post
        response = self.client.post(home_url, {'initial_code': ''},
                                    HTTP_ACCEPT_ENCODING='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Request.objects.count(), 0)
        # proper form post
        with self.assertTemplateUsed('core/home.json'):
            response = self.client.post(home_url, {'initial_code': 'foo'},
                    follow=True, HTTP_ACCEPT_ENCODING='application/json')
        self.assertEqual(response['Content-Type'],
                         'application/json; charset=utf-8')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Request.objects.count(), 1)  # creates a request
