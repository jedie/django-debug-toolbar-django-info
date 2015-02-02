#!/usr/bin/env python

"""
    django-info-panel
    ~~~~~~~~~~~~~~~~~

    :copyleft: 2015 by the django-debug-toolbar-django-info team, see AUTHORS for more details.
    :created: 2015 by JensDiemer.de
    :license: GNU GPL v3 or above, see LICENSE for more details.
"""

from __future__ import absolute_import, unicode_literals

import logging

from django.db import backend, connection
from django.db.models.loading import get_apps, get_models
from django.utils.translation import ugettext_lazy as _

from debug_toolbar.panels import Panel

logger = logging.getLogger(__name__)


class DatabaseInfo(Panel):
    nav_title = _("Database")
    title=_("Database Information")
    template = 'django_info/panels/database.html'

    def process_response(self, request, response):
        apps_info = []
        for app in get_apps():
            model_info = []
            for model in get_models(app):
                model_info.append({
                    "name":model._meta.object_name,
                })
            apps_info.append({
                "app_name": app.__name__,
                "app_models": model_info,
            })

        self.record_stats({
            "db_backend_name": backend.Database.__name__,
            "db_backend_module": backend.Database.__file__,
            "db_backend_version": getattr(backend.Database, "version", "?"),

            "apps_info": apps_info,

            "db_table_names": sorted(connection.introspection.table_names()),
            "django_tables": sorted(connection.introspection.django_table_names()),
        })

