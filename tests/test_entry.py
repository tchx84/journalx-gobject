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

import sys

from gi.repository import GObject

sys.path.append("..")
from journalx.setting import Setting
from journalx.entry import Entry


Setting.set_url('http://localhost:8000')

def __phase1_failed_cb(entry, info):
    print '[FAILED] phase1: entries-posted-failed, with %s' % info
    loop.quit()

def __phase2_failed_cb(entry, info):
    print '[FAILED] phase2: entries-downloaded-failed, with %s' % info
    loop.quit()

def __phase3_failed_cb(entry, info):
    print '[FAILED] phase3: entries-updated-failed, with %s' % info
    loop.quit()

def __phase4_failed_cb(entry, info):
    print '[FAILED] phase4: screenshot-downloaded-failed, with %s' % info
    loop.quit()

def __phase5_failed_cb(entry, info):
    print '[FAILED] phase5: entries-deleted-failed, with %s' % info
    loop.quit()


def __phase1_cb(entry, info):
    print '[OK] phase1: entries-posted, with: \n%s\n' % info
    
    entry.connect('entry-downloaded', __phase2_cb)
    entry.connect('entry-downloaded-failed', __phase2_failed_cb)
    entry.get()

def __phase2_cb(entry, info):
    print '[OK] phase2: entry-downloaded, with: \n%s\n' % info

    entry.connect('entry-updated', __phase3_cb)
    entry.connect('entry-updated-failed', __phase3_failed_cb)
    entry.update('new-title', 'new-description', 'screenshot.png')

def __phase3_cb(entry, info):
    print '[OK] phase3: entry-updated, with: \n%s\n' % info

    entry.connect('screenshot-downloaded', __phase4_cb)
    entry.connect('screenshot-downloaded-failed', __phase4_failed_cb)
    entry.screenshot()

def __phase4_cb(entry, info):
    print '[OK] phase4: screenshot-downloaded, with: \nsize %d\n' % len(info)

    entry.connect('entry-deleted', __phase5_cb)
    entry.connect('entry-deleted-failed', __phase5_failed_cb)
    entry.delete()

def __phase5_cb(entry, info):
    print '[OK] phase5: entries-deleted, with: \n%s\n' % info
    loop.quit()

entry = Entry()
entry.connect('entry-posted', __phase1_cb)
entry.connect('entry-posted-failed', __phase1_failed_cb)
entry.post('title', 'description', 'screenshot.png')

loop = GObject.MainLoop()
loop.run()
