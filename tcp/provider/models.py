#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _


class Provider(models.Model):
    """Video provider."""
    name = models.CharField(max_length=50,
                            help_text=_("Name of the video provider"))
    link_template = models.TextField(help_text=_("Template to render for the "
                                                  "full video link"))
    embed_template = models.TextField(help_text=_("Template to render for the "
                                                  "embed code"))

    class meta:
        ordering = ['name']

    def __unicode__(self):
        return self.name


class LinkMatch(models.Model):
    """Regex pattern to match a video id."""
    provider = models.ForeignKey(Provider,
                                 help_text=_("Video provider for this match"))
    pattern = models.CharField(max_length=255,
                               help_text=_("Regex to match the embed code "
                                           "against, and get the video id"))

    class meta:
        ordering = ['provider__name']

    def __unicode__(self):
        return self.provider.name
