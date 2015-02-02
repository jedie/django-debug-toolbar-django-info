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

from django.conf import settings
from django.contrib.admindocs.views import simplify_regex
from django.core.exceptions import ViewDoesNotExist
from django.core.urlresolvers import RegexURLPattern, RegexURLResolver
from django.utils.translation import ugettext_lazy as _

from debug_toolbar.panels import Panel

logger = logging.getLogger(__name__)



class UrlPatternInfo(object):
    """
    most parts borrowed from django-extensions:
    https://github.com/django-extensions/django-extensions/blob/master/django_extensions/management/commands/show_urls.py
    """
    def _get_root_urlpatterns(self):
        urlconf = __import__(settings.ROOT_URLCONF, {}, {}, [''])
        urlpatterns = urlconf.urlpatterns
        return urlpatterns

    def get_url_info(self, urlpatterns=None):
        """
        return a dict-list of the current used url patterns
        """
        if urlpatterns is None:
            urlpatterns = self._get_root_urlpatterns()

        view_functions = self._extract_views_from_urlpatterns(urlpatterns)

        url_info = []
        for (func, regex, url_name) in view_functions:
            if hasattr(func, '__name__'):
                func_name = func.__name__
            elif hasattr(func, '__class__'):
                func_name = '%s()' % func.__class__.__name__
            else:
                func_name = re.sub(r' at 0x[0-9a-f]+', '', repr(func))
            url = simplify_regex(regex)

            url_info.append({
                'func_name': func_name,
                'module': func.__module__,
                'url_name': url_name,
                'regex': regex,
                'url': url
            })
        return url_info

    def _extract_views_from_urlpatterns(self, urlpatterns, base=''):
        """
        Return a list of views from a list of urlpatterns.

        Each object in the returned list is a two-tuple: (view_func, regex)
        """
        views = []
        for p in urlpatterns:
            if isinstance(p, RegexURLPattern):
                try:
                    views.append((p.callback, base + p.regex.pattern, p.name))
                except ViewDoesNotExist:
                    continue
            elif isinstance(p, RegexURLResolver):
                try:
                    patterns = p.url_patterns
                except ImportError:
                    continue
                views.extend(self._extract_views_from_urlpatterns(patterns, base + p.regex.pattern))
            elif hasattr(p, '_get_callback'):
                try:
                    views.append((p._get_callback(), base + p.regex.pattern, p.name))
                except ViewDoesNotExist:
                    continue
            elif hasattr(p, 'url_patterns') or hasattr(p, '_get_url_patterns'):
                try:
                    patterns = p.url_patterns
                except ImportError:
                    continue
                views.extend(self._extract_views_from_urlpatterns(patterns, base + p.regex.pattern))
            else:
                raise TypeError("%s does not appear to be a urlpattern object" % p)
        return views


class UrlPatternsInfo(Panel):
    nav_title = _("URL-Patterns")
    title=_("URL-Patterns Information")
    template = 'django_info/panels/urlpatterns.html'

    def process_response(self, request, response):
        # Information about the current used url patterns
        urlpatterns = UrlPatternInfo().get_url_info()

        self.record_stats({
            "urlpatterns": urlpatterns,
        })

