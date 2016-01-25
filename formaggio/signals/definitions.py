# -*- coding: utf-8 -*-
import django.dispatch

form_answered = django.dispatch.Signal(providing_args=['form', 'form_result'])
