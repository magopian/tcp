#!/usr/bin/env python
# -*- coding: utf-8 -*-

import floppyforms as forms

from .models import Request


class RequestForm(forms.ModelForm):
    class Meta:
        fields = ['initial_code']
        model = Request
        #widgets = {'initial_code': forms.Textarea}
