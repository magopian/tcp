#!/usr/bin/env python
# -*- coding: utf-8 -*-

from json import loads, dumps

from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client
from django.utils.translation import ugettext_lazy as _

from tcp.provider.models import Provider, LinkMatch

from .models import Request
from .views import validate


class Helper(object):
    """Mock the requests.head calls."""

    def __init__(self, status_code):
        self.status_code = status_code

    def head(self, link):
        return self


class RequestTest(TestCase):
    """Test the request"""

    def setUp(self):
        super(RequestTest, self).setUp()
        self.provider = Provider.objects.create(
                name='Foo',
                link_template='http://{{ video_id }}',
                embed_template='some code {{ video_link }}',
                validation_link_template='http://httpbin.org/status/'
                                         '{{video_id }}')
        LinkMatch.objects.create(provider=self.provider,
                                 pattern='foo_video/(.*)')

    def test_match(self):
        """Match a provider."""
        # matching request
        request = Request(initial_code='some stuff foo_video/barbaz')
        request.match()
        self.assertEqual(request.video_id, 'barbaz')
        self.assertEqual(request.provider, self.provider)
        # matching request ignore case
        request = Request(initial_code='some stuff FOO_VIDEO/barbaz')
        request.match()
        self.assertEqual(request.video_id, 'barbaz')
        self.assertEqual(request.provider, self.provider)
        # matching request multiline
        request = Request(initial_code='some stuff\nFOO_VIDEO/barbaz')
        request.match()
        self.assertEqual(request.video_id, 'barbaz')
        self.assertEqual(request.provider, self.provider)
        # non matching request
        request = Request(initial_code='some stuff video/barbaz')
        request.match()
        self.assertEqual(request.video_id, '')
        self.assertIsNone(request.provider)

    def test_get_link(self):
        """Compute full video link."""
        request = Request(initial_code='_',
                          video_id='bar',
                          provider=self.provider)
        link = request.get_link()
        self.assertEqual(link, 'http://bar')

    def test_get_clean_code(self):
        """Compute the new embed code."""
        request = Request(initial_code='_',
                          video_id='bar',
                          provider=self.provider)
        link = request.get_clean_code()
        self.assertEqual(link, 'some code http://bar')

    def test_validate(self):
        """Validate the video link."""
        request = Request(initial_code='_',
                          video_id='foo',
                          provider=self.provider)
        self.assertTrue(request.validate(helper=Helper(200)))
        self.assertTrue(request.validate(helper=Helper(301)))
        self.assertFalse(request.validate(helper=Helper(400)))

    def test_save(self):
        """Process a request"""
        # matching request
        request = Request(initial_code='stuff foo_video/barbaz')
        request.save()
        self.assertEqual(request.video_id, 'barbaz')
        self.assertEqual(request.provider, self.provider)
        # non matching request
        request = Request(initial_code='stuff video/barbaz')
        request.save()
        self.assertEqual(request.video_id, '')
        self.assertIsNone(request.provider)


class RequestViewTest(TestCase):
    """Test the views"""

    def setUp(self):
        self.client = Client()
        self.provider = Provider.objects.create(
                name='Foo',
                link_template='http://{{ video_id }}',
                embed_template='some code {{ video_link }}',
                validation_link_template='http://httpbin.org/status/'
                                         '{{video_id }}')
        LinkMatch.objects.create(provider=self.provider,
                                 pattern='foo_video/(.*)')
        self.home_url = reverse('core:home')

    def test_create_view(self):
        """Create view"""
        self.assertEqual(Request.objects.count(), 0)
        # invalid form post
        with self.assertTemplateUsed('core/home.html'):
            response = self.client.post(self.home_url, {'initial_code': ''})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Request.objects.count(), 0)
        # proper form post
        with self.assertTemplateUsed('core/request_detail.html'):
            response = self.client.post(
                    self.home_url,
                    {'initial_code': 'some stuff foo_video/barbaz'},
                    follow=True)
        self.assertEqual(Request.objects.count(), 1)  # creates a request
        request = Request.objects.all()[0]
        cleaned_url = reverse('core:cleaned', kwargs={'pk': request.pk})
        self.assertRedirects(response, cleaned_url)
        self.assertContains(response, "Video link")

    def test_create_view_json(self):
        """Create view, with 'Accept' header set to json"""
        self.assertEqual(Request.objects.count(), 0)
        # invalid form post
        response = self.client.post(self.home_url, {'initial_code': ''},
                                    HTTP_ACCEPT_ENCODING='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Request.objects.count(), 0)
        # proper form post
        response = self.client.post(
                self.home_url,
                {'initial_code': 'some stuff foo_video/barbaz'},
                follow=True,
                HTTP_ACCEPT_ENCODING='application/json')
        self.assertEqual(response['Content-Type'],
                         'application/json; charset=utf-8')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Request.objects.count(), 1)  # creates a request
        self.assertContains(response, "video_id")
        self.assertTrue(loads(response.content))  # json can be decoded

    def test_validate_view_unknown_provider(self):
        validate_url = reverse('core:validate', kwargs={'provider': 'unknown',
                                                        'video_id': 'foo'})
        response = self.client.get(validate_url)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, _("Provider not found"))

    def test_validate_view_valid_video(self):
        response = validate(request=None, provider='Foo', video_id='foo',
                            helper=Helper(200))
        data = {'valid': 'true'}
        self.assertEqual(response.content, dumps(data))
        response = validate(request=None, provider='Foo', video_id='foo',
                            helper=Helper(301))
        self.assertEqual(response.content, dumps(data))

    def test_validate_view_invalid_video(self):
        response = validate(request=None, provider='Foo', video_id='foo',
                            helper=Helper(404))
        data = {'valid': 'false'}
        self.assertEqual(response.content, dumps(data))
