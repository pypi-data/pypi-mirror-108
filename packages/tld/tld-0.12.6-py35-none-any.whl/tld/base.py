
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from six import with_metaclass as _py_backwards_six_withmetaclass
from codecs import open as codecs_open
import logging
try:
    from urllib.request import urlopen
except ImportError:
    from six.moves.urllib.request import urlopen as urlopen
from typing import Optional, Dict, Union, ItemsView
from .exceptions import TldIOError, TldImproperlyConfigured
from .helpers import project_dir
__author__ = u'Artur Barseghyan'
__copyright__ = u'2013-2021 Artur Barseghyan'
__license__ = u'MPL-1.1 OR GPL-2.0-only OR LGPL-2.1-or-later'
__all__ = (u'BaseTLDSourceParser', u'Registry')
LOGGER = logging.getLogger(__name__)


class Registry(type):
    REGISTRY = {

    }

    def __new__(mcs, name, bases, attrs):
        new_cls = type.__new__(mcs, name, bases, attrs)
        if getattr(new_cls, u'_uid', None):
            mcs.REGISTRY[new_cls._uid] = new_cls
        return new_cls

    @property
    def _uid(cls):
        return getattr(cls, u'uid', cls.__name__)

    @classmethod
    def reset(mcs):
        mcs.REGISTRY = {

        }

    @classmethod
    def get(mcs, key, default=None):
        return mcs.REGISTRY.get(key, default)

    @classmethod
    def items(mcs):
        return mcs.REGISTRY.items()


class BaseTLDSourceParser(
        _py_backwards_six_withmetaclass(Registry, *[object])):
    u'Base TLD source parser.'
    uid = None
    include_private = True

    @classmethod
    def validate(cls):
        u'Constructor.'
        if (not cls.uid):
            raise TldImproperlyConfigured(
                u'The `uid` property of the TLD source parser shall be defined.')

    @classmethod
    def get_tld_names(cls, fail_silently=False, retry_count=0):
        u'Get tld names.\n\n        :param fail_silently:\n        :param retry_count:\n        :return:\n        '
        cls.validate()
        raise NotImplementedError(
            u'Your TLD source parser shall implement `get_tld_names` method.')

    @classmethod
    def update_tld_names(cls, fail_silently=False):
        u'Update the local copy of the TLD file.\n\n        :param fail_silently:\n        :return:\n        '
        try:
            remote_file = urlopen(cls.source_url)
            local_file_abs_path = project_dir(cls.local_path)
            local_file = codecs_open(
                local_file_abs_path, u'wb', encoding=u'utf8')
            local_file.write(remote_file.read().decode(u'utf8'))
            local_file.close()
            remote_file.close()
            LOGGER.debug(u''.join([u"Fetched '", u'{}'.format(
                cls.source_url), u"' as '", u'{}'.format(local_file_abs_path), u"'"]))
        except Exception as err:
            LOGGER.debug(u''.join([u"Failed fetching '", u'{}'.format(
                cls.source_url), u"'. Reason: ", u'{}'.format(str(err))]))
            if fail_silently:
                return False
            raise TldIOError(err)
        return True
