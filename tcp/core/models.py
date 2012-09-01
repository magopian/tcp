#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

from django.db import models
from django.template import Context, Template
from django.utils.translation import ugettext_lazy as _

from tcp.provider.models import Provider, LinkMatch


class Request(models.Model):
    """Request for a video embed code."""
    initial_code = models.TextField(help_text=_("Requested video embed code"))
    video_link = models.URLField(
            max_length=200, blank=True,
            help_text=_("Full video link (cannonical)"))
    is_valid = models.BooleanField(
            default=False,
            help_text=_("Is the video still valid?"))
    clean_code = models.TextField(
            blank=True,
            help_text=_("Cleaned video embed code"))
    message = models.CharField(
            max_length=255, blank=True,
            help_text=_("Log message on what was done"))
    provider = models.ForeignKey(
            Provider, null=True, blank=True,
            help_text=_("Provider of this video"))

    class meta:
        ordering = ['-id']

    def __unicode__(self):
        return unicode(self.pk)

    def save(self, *args, **kwargs):
        """Save the request to the database, and try to validate it."""
        video_id, provider = self.match()
        if provider is not None:
            self.provider = provider
            self.video_link = self.get_link(video_id, provider)
            self.clean_code = self.get_clean_code(self.video_link, provider)
        else:
            self.message = _("No provider found for this video")
        super(Request, self).save(*args, **kwargs)

    def match(self):
        """Return [video_id, provider] or None from an embed code"""
        for lm in LinkMatch.objects.all():  # loop over all possible patterns
            res = re.search(lm.pattern, self.initial_code,
                                flags=re.IGNORECASE | re.MULTILINE)
            if res:
                return [res.groups()[0], lm.provider]
        return [None, None]

    def get_link(self, video_id, provider):
        """Return the full video link from a video id and a provider."""
        template = Template(provider.link_template)
        return template.render(Context({'video_id': video_id}))

    def get_clean_code(self, video_link, provider):
        """Return the new embed code from a video link and a provider."""
        template = Template(provider.embed_template)
        return template.render(Context({'video_link': video_link}))
