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


class Comment(JObject):

    POST_URL = '/entries/%s/comments/'
    DELETE_URL = '/entries/%s/comments/%s'

    def __init__(self, entry_id, comment_id=None):
        JObject.__init__(self, comment_id)
        self._entry_id = entry_id

    @asynchronous
    @check_is_not_created
    def post(self, text):
        self._post(self._url(self.POST_URL % self._entry_id),
                   self._params(text),
                   None)

    @asynchronous
    @check_is_created
    def delete(self):
        self._delete(self._url(self.DELETE_URL % (self._entry_id, self.id)))

    def _params(self, text):
        params = []
        params += [('entry_id', (self._entry_id))]
        params += [('text', (text))]
        return params
