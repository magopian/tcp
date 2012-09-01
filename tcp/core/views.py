#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse_lazy
from django.views.generic import CreateView

from .forms import RequestForm


create_view = CreateView.as_view(form_class=RequestForm,
                                 success_url=reverse_lazy('core:home'),
                                 template_name='core/home.html')
