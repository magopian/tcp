#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseBadRequest
from django.shortcuts import render
from django.views.generic import CreateView

from .forms import RequestForm


class RequestCreateView(CreateView):
    """Customized create view for Requests"""

    def form_invalid(self, form):
        """If json (api), return json"""
        if self.request.META.get('HTTP_ACCEPT_ENCODING') == 'application/json':
            return HttpResponseBadRequest()
        return super(RequestCreateView, self).form_invalid(form)

    def form_valid(self, form):
        """If json (api), return json"""
        res = super(RequestCreateView, self).form_valid(form)  # create object
        if self.request.META.get('HTTP_ACCEPT_ENCODING') == 'application/json':
            return render(self.request, 'core/home.json',
                          {'object': self.object},
                          content_type='application/json; charset=utf-8')
        return res

create_view = RequestCreateView.as_view(form_class=RequestForm,
                                        success_url=reverse_lazy('core:home'),
                                        template_name='core/home.html')
