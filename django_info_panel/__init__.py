# coding: utf-8
"""
    django-info-panel
    ~~~~~~~~~~~~~~~~~

    :copyleft: 2015 by the django-debug-toolbar-django-info team, see AUTHORS for more details.
    :created: 2015 by JensDiemer.de
    :license: GNU GPL v3 or above, see LICENSE for more details.
"""

from __future__ import absolute_import, division, print_function

__version__ = (0,2,0)


VERSION_STRING = '.'.join(str(part) for part in __version__)


if __name__ == "__main__":
    print(VERSION_STRING)
