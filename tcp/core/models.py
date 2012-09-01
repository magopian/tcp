#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

from django.db import models
from django.utils.translation import ugettext_lazy as _

from tcp.provider.models import Provider, LinkMatch


class Request(models.Model):
    """Request for a video embed code"""
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

    def match(self):
        """Match a video embed code to a provider, or return False"""
        for lm in LinkMatch.objects.all():  # loop over all possible patterns
            res = re.search(lm.pattern, self.initial_code,
                            flags=re.IGNORECASE|re.MULTILINE)
            if res:
                self.provider = lm.provider
                self.save()
                return res
        else:  # no match found
            self.message = _("No provider found")
            self.save()
        return False
