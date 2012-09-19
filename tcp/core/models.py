#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

from django.db import models
from django.template import Context, Template
from django.utils.translation import ugettext_lazy as _
import requests

from tcp.provider.models import Provider, LinkMatch


class Request(models.Model):
    """Request for a video embed code."""
    initial_code = models.TextField(help_text=_("Requested video embed code"))
    video_id = models.CharField(
            max_length=255, blank=True,
            help_text=_("Used to construct video link and embed code"))
    provider = models.ForeignKey(
            Provider, null=True, blank=True,
            help_text=_("Provider of this video"))

    class meta:
        ordering = ['-id']

    def __unicode__(self):
        return unicode(self.pk)

    def save(self, *args, **kwargs):
        """Save the request to the database, and try match it to a provider."""
        self.match()
        super(Request, self).save(*args, **kwargs)

    def match(self):
        """Set the video_id and provider if found from the embed code."""
        for lm in LinkMatch.objects.all():  # loop over all possible patterns
            res = re.search(lm.pattern, self.initial_code,
                                flags=re.IGNORECASE | re.MULTILINE)
            if res:
                self.video_id = res.groups()[0]
                self.provider = lm.provider

    def get_link(self):
        """Return the full video link from a video id and a provider."""
        if not self.video_id:
            return
        template = Template(self.provider.link_template)
        return template.render(Context({'video_id': self.video_id}))

    def get_clean_code(self):
        """Return the new embed code from a video link and a provider."""
        if not self.video_id:
            return
        template = Template(self.provider.embed_template)
        return template.render(Context({'video_link': self.get_link()}))

    def validate(self):
        """True if the status code of the url is less than 400."""
        if not self.video_id:
            return
        template = Template(self.provider.validation_link_template)
        video_link = template.render(Context({'video_id': self.video_id}))
        try:
            req = requests.head(video_link)
            return req.status_code < 400
        except:
            return False
