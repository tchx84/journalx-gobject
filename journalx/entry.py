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

from jobject import JObject
from grestful.decorators import asynchronous
from grestful.decorators import check_is_created
from grestful.decorators import check_is_not_created
from grestful.helpers import param_upload


class Entry(JObject):

    POST_URL = '/entries/'
    UPDATE_URL = '/entries/%s'
    GET_URL = '/entries/%s'
    DELETE_URL = '/entries/%s'
    COMMENTS_URL = '/entries/%s/comments/'
    SCREENSHOT_URL = '/entries/%s/screenshot'

    @asynchronous
    @check_is_not_created
    def post(self, title, desc, screenshot_path):
       self._post(self._url(self.POST_URL),
                  self._params(title, desc),
                  param_upload('screenshot', screenshot_path))

    @asynchronous
    @check_is_created
    def update(self, title=None, desc=None, screenshot_path=None):
        self._post(self._url(self.UPDATE_URL % self.id),
                   self._params(title, desc),
                   param_upload('screenshot', screenshot_path))

    @asynchronous
    @check_is_created
    def get(self):
        self._get(self._url(self.GET_URL % self.id), None)

    @asynchronous
    @check_is_created
    def delete(self):
        self._delete(self._url(self.DELETE_URL % self.id))

    @asynchronous
    @check_is_created
    def comments(self):
        self._get(self._url(self.COMMENTS_URL % self.id), None)

    @asynchronous
    @check_is_created
    def screenshot(self):
        self._get(self._url(self.SCREENSHOT_URL % self.id), None)

    def _params(self, title=None, desc=None):
        params = []
        if title is not None:
            params += [('title', (title))]
        if desc is not None:
            params += [('desc', (desc))]

        return params
