#!/usr/bin/env python
# -*- coding: utf-8 -*-

from json import dumps

from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseBadRequest, HttpResponse
from django.utils.translation import ugettext_lazy as _
from django.views.generic import CreateView, DetailView
import requests

from tcp.provider.models import Provider
from .forms import RequestForm
from .models import Request


class RequestCreateView(CreateView):
    """Customized create view for Requests."""
    form_class = RequestForm
    success_url = reverse_lazy('core:cleaned')
    template_name = 'core/home.html'

    def form_invalid(self, form):
        """If json (api), return json."""
        if self.request.META.get('HTTP_ACCEPT_ENCODING') == 'application/json':
            return HttpResponseBadRequest()
        return super(RequestCreateView, self).form_invalid(form)

    def form_valid(self, form):
        """If json (api), return json"""
        res = super(RequestCreateView, self).form_valid(form)  # create object
        if self.request.META.get('HTTP_ACCEPT_ENCODING') == 'application/json':
            data = {'video_id': self.object.video_id,
                    'provider': unicode(self.object.provider),
                    'video_link': self.object.get_link(),
                    'clean_code': self.object.get_clean_code(),
                    'is_valid': 'true' if self.object.validate() else 'false'}
            return HttpResponse(dumps(data),
                                content_type='application/json; charset=utf-8')
        return res

    def get_success_url(self):
        return reverse_lazy('core:cleaned', kwargs={'pk': self.object.pk})
create_view = RequestCreateView.as_view()

detail_view = DetailView.as_view(model=Request)


def validate(request, provider, video_id, helper=requests):
    """Return True if the video is still available."""
    try:
        provider = Provider.objects.get(name=provider)
    except Provider.DoesNotExist:
        return HttpResponseBadRequest(_("Provider not found"))
    req = Request(provider_id=provider.pk, video_id=video_id)
    data = {'valid': 'true' if req.validate(helper=helper) else 'false'}
    return HttpResponse(dumps(data),
                        content_type='application/json; charset=utf-8')
