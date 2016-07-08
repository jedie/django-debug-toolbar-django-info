#!/usr/bin/env python

"""
    django-info-panel
    ~~~~~~~~~~~~~~~~~

    :copyleft: 2015-2016 by the django-debug-toolbar-django-info team, see AUTHORS for more details.
    :created: 2015 by JensDiemer.de
    :license: GNU GPL v3 or above, see LICENSE for more details.
"""

from __future__ import absolute_import, unicode_literals

import logging

from django.db import connection
from django.apps import apps
from django.utils.translation import ugettext_lazy as _

from debug_toolbar.panels import Panel

logger = logging.getLogger(__name__)


class DatabaseInfo(Panel):
    nav_title = _("Database")
    title=_("Database Information")
    template = 'django_info/panels/database.html'

    def process_response(self, request, response):
        apps_info = []
        app_configs = apps.get_app_configs()
        for app_config in app_configs:
            models = app_config.get_models()
            model_info = []
            for model in models:
                model_info.append({
                    "name":model._meta.object_name,
                })
            apps_info.append({
                "app_name": app_config.name,
                "app_models": model_info,
            })

        self.record_stats({
            "db_backend_name": connection.Database.__name__,
            "db_backend_module": connection.Database.__file__,
            "db_backend_version": getattr(connection.Database, "version", "?"),

            "apps_info": apps_info,

            "db_table_names": sorted(connection.introspection.table_names()),
            "django_tables": sorted(connection.introspection.django_table_names()),
        })

