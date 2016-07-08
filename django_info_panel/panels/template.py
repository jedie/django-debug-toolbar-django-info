#!/usr/bin/env python

"""
    django-info-panel
    ~~~~~~~~~~~~~~~~~

    :copyleft: 2015-2016 by the django-debug-toolbar-django-info team, see AUTHORS for more details.
    :created: 2015 by JensDiemer.de
    :license: GNU GPL v3 or above, see LICENSE for more details.
"""

from __future__ import absolute_import, unicode_literals

import fnmatch
import sys
import os

if __name__ == "__main__":
    # run directly
    sys.path.insert(0, os.path.expanduser("~/page_instance"))
    os.environ["DJANGO_SETTINGS_MODULE"] = "example_project.settings"

import inspect
import logging

import django
from django.template.base import get_library, get_templatetags_modules
from django.utils.translation import ugettext_lazy as _


from debug_toolbar.panels import Panel

logger = logging.getLogger(__name__)


class TemplateTagInfo(object):
    def __init__(self, name):
        name=name

def collect_docs(items):
    data = {}
    for item in items:
        doc = inspect.getdoc(items[item]) or ""
        if doc:
            doc = inspect.cleandoc(doc)
        data[item] = doc
    return data



def get_templateinfo():
    modules = get_templatetags_modules()

    template_info = {}
    for module in modules:
        try:
            templatetag_mod = __import__(module, {}, {}, [''])
        except Exception as err:
            logger.debug("Can't import %r: %s" % (module, err))
            continue

        mod_path = os.path.dirname(inspect.getabsfile(templatetag_mod))
        tag_files = [
            os.path.splitext(fn)[0]
            for fn in os.listdir(mod_path)
            if fnmatch.fnmatch(fn, "*.py") and not fn.startswith("_")
        ]

        lib_info = {}
        for taglib in tag_files:
            try:
                lib = get_library(taglib)
            except:
                continue

            lib_info[taglib] = {
                "tags": collect_docs(lib.tags),
                "filters": collect_docs(lib.filters),
            }

        template_info[module.split(".")[0]] = lib_info

    return template_info




class TemplateInfo(Panel):
    nav_title = _("Template Info")
    title=_("Template Tags/Filters Information")
    template = 'django_info/panels/template.html'

    def process_response(self, request, response):
        self.record_stats({
            "template_info": get_templateinfo(),
        })


if __name__=="__main__":
    from pprint import pprint
    django.setup()
    template_info = get_templateinfo()

    pprint(template_info)
