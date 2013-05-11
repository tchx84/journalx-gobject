# Copyright (c) 2013 Martin Abente Lahaye. - tch@sugarlabs.org
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA 02110-1301 USA.

import json
import logging

import error
from object import Object
from setting import Setting


class ObjectPlus(Object):

    def __init__(self, id=None):
      Object.__init__(self)
      self._id = id

    def _get(self, url, params, completed_data, failed_data):
        completed_id = self.connect('transfer-completed',
                                    self._completed_cb, completed_data)
        failed_id = self.connect('transfer-failed',
                                 self._failed_cb, failed_data)
        self.request('GET', Setting.get_url(url), params)
        self.disconnect(completed_id)
        self.disconnect(failed_id)

    def _post(self, url, params, file, completed_data, failed_data):
        completed_id = self.connect('transfer-completed',
                                    self._completed_cb, completed_data)
        failed_id = self.connect('transfer-failed',
                                 self._failed_cb, failed_data)
        self.request('POST', Setting.get_url(url), params, file)
        self.disconnect(completed_id)
        self.disconnect(failed_id)

    def _delete(self, url, completed_data, failed_data):
        completed_id = self.connect('transfer-completed',
                                    self._completed_cb, completed_data)
        failed_id = self.connect('transfer-failed',
                                 self._failed_cb, failed_data)
        self.request('DELETE', Setting.get_url(url))
        self.disconnect(completed_id)
        self.disconnect(failed_id)

    def _completed_cb(self, object, data, signal):
        try:
            info = json.loads(data)
            self._id_hook(info)
            self.emit(signal, info)
        except Exception, e:
            logging.error('%s: _completed_cb crashed with %s',
                          self.__class__.__name__, str(e))

    def _failed_cb(self, object, message, signal):
        self.emit(signal, message)

    def _id_hook(self, info):
        if isinstance(info, dict) and 'id' in info.keys():
            self._id = info['id']

    def _file(self, field, path):
        if not path:
            return None

        file = {}
        file['field'] =  field
        file['path'] = path

        return file

    def _check_is_not_created(self):
        if self._id is not None:
            raise error.AlreadyCreated('Already created')

    def _check_is_created(self):
        if self._id is None:
            raise error.NotCreated('Not created')
