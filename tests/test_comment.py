#!/usr/bin/env python
#
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

import uuid
import sys

from gi.repository import GObject

sys.path.append("..")
from journalx.setting import Setting
from journalx.entry import Entry
from journalx.comment import Comment


Setting.set_url('http://localhost:8000')
Setting.set_buddy_credential(uuid.uuid1())

def __phase1_failed_cb(entry, info):
    print '[FAILED] phase1: entries posted failed, with %s' % info
    loop.quit()

def __phase2_failed_cb(comment, info, entry):
    print '[FAILED] phase2: comment posted failed, with %s' % info
    clean(entry)

def __phase3_failed_cb(entry, info):
    print '[FAILED] phase3: comments downloaded failed, with %s' % info
    clean(entry)

def __phase4_failed_cb(comment, info, entry):
    print '[FAILED] phase4: comment deleted failed, with %s' % info
    clean(entry)

def __cleaning_failed_cb(entry, info):
    print '[FAILED] cleaning: entry deleted failed, with %s' % info
    loop.quit()

def __phase1_cb(entry, info):
    print '[OK] phase1: entry posted, with: \n%s\n' % info

    entry_id = str(entry.id)

    comment = Comment(entry_id)
    comment.connect('completed', __phase2_cb, entry)
    comment.connect('failed', __phase2_failed_cb, entry)
    comment.post('text')

def __phase2_cb(comment, info, entry):
    print '[OK] phase2: comment posted, with: \n%s\n' % info

    id = entry.id

    entry = Entry(id)
    entry.connect('completed', __phase3_cb)
    entry.connect('failed', __phase3_failed_cb)
    entry.comments()

def __phase3_cb(entry, info):
    print '[OK] phase3: comments downloaded, with: \n%s\n' % info

    entry_id = info[0]['entry_id']
    comment_id = info[0]['id']

    comment = Comment(entry_id, comment_id)
    comment.connect('completed', __phase4_cb, entry)
    comment.connect('failed', __phase4_failed_cb, entry)
    comment.delete()

def __phase4_cb(comment, info, entry):
    print '[OK] phase4: comment deleted, with: \n%s\n' % info
    clean(entry)

def __cleaning_cb(entry, info):
    print '[OK] cleaning: entry deleted, with: \n%s\n' % info
    loop.quit()

def clean(entry):
  id = entry.id

  entry = Entry(id)
  entry.connect('completed', __cleaning_cb)
  entry.connect('failed', __cleaning_failed_cb)
  entry.delete()

entry = Entry()
entry.connect('completed', __phase1_cb)
entry.connect('failed', __phase1_failed_cb)
entry.post('title', 'description', 'screenshot.png')

loop = GObject.MainLoop()
loop.run()
