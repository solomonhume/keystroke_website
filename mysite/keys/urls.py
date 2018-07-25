# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig

from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^prof', views.prof, name = 'prof'),
    url(r'^listen', views.listen, name = 'listen'),
    url(r'^listn2', views.listn2, name = 'listn2'),
    url(r'test', views.test, name = 'test'),
    url(r'^result', views.result, name = 'result')
]