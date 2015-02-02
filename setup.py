#!/usr/bin/env python
# coding: utf-8
"""
    django-info-panel
    ~~~~~~~~~~~~~~~~~

    :copyleft: 2015 by the django-debug-toolbar-django-info team, see AUTHORS for more details.
    :created: 2015 by JensDiemer.de
    :license: GNU GPL v3 or above, see LICENSE for more details.
"""

from __future__ import absolute_import, division, print_function


import os
import sys

from setuptools import setup, find_packages

from django_info_panel import VERSION_STRING


PACKAGE_ROOT = os.path.dirname(os.path.abspath(__file__))


# convert creole to ReSt on-the-fly, see also:
# https://code.google.com/p/python-creole/wiki/UseInSetup
try:
    from creole.setup_utils import get_long_description
except ImportError as err:
    if "check" in sys.argv or "register" in sys.argv or "sdist" in sys.argv or "--long-description" in sys.argv:
        raise ImportError("%s - Please install python-creole >= v0.8 - e.g.: pip install python-creole" % err)
    long_description = None
else:
    long_description = get_long_description(PACKAGE_ROOT)


def get_authors():
    try:
        with open(os.path.join(PACKAGE_ROOT, "AUTHORS"), "r") as f:
            authors = [l.strip(" *\r\n") for l in f if l.strip().startswith("*")]
    except Exception as err:
        authors = "[Error: %s]" % err
    return authors



setup_info = dict(
    name='django-debug-toolbar-django-info',
    version=VERSION_STRING,
    description='django-info panel for django-debug-toolbar',
    long_description=long_description,
    author=get_authors(),
    maintainer="Jens Diemer",
    url='https://github.com/jedie/django-debug-toolbar-django-info',
    download_url = 'https://github.com/jedie/django-debug-toolbar-django-info',
    packages=find_packages(
        #exclude=[".project", ".pydevproject", "pylucid_project.external_plugins.*"]
    ),
    include_package_data=True, # include package data under version control
    zip_safe=False,
    classifiers=[
        'Development Status :: 3 - Alpha',
#         "Development Status :: 4 - Beta",
#         "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Programming Language :: Python",
        "Programming Language :: JavaScript",
        'Framework :: Django',
        "Topic :: Database :: Front-Ends",
        "Topic :: Documentation",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Internet :: WWW/HTTP :: Site Management",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        "Operating System :: OS Independent",
    ]
)
setup(**setup_info)
