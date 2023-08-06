# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import unittest
__author__ = u'Artur Barseghyan'
__copyright__ = u'2013-2021 Artur Barseghyan'
__license__ = u'MPL-1.1 OR GPL-2.0-only OR LGPL-2.1-or-later'
__all__ = (u'TestRegistry',)


class TestRegistry(unittest.TestCase):
    u'Test registry.'

    def test_import_from_registry(self):
        u'Test import from deprecated `valuta.registry` module.'
        from ..registry import Registry
