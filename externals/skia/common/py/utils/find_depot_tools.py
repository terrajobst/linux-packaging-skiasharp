# Copyright (c) 2012 The Chromium Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.
"""Small utility function to find depot_tools and add it to the python path.

Will throw an ImportError exception if depot_tools can't be found since it
imports breakpad.

This file is directly copied from:
https://chromium.googlesource.com/chromium/tools/build/+/master/scripts/common/find_depot_tools.py
"""

import os
import sys


def directory_really_is_depot_tools(directory):
  return os.path.isfile(os.path.join(directory, 'breakpad.py'))


def add_depot_tools_to_path():
  """Search for depot_tools and add it to sys.path."""
  # First look if depot_tools is already in PYTHONPATH.
  for i in sys.path:
    if i.rstrip(os.sep).endswith('depot_tools'):
      if directory_really_is_depot_tools(i):
        return i

  # Then look if depot_tools is in PATH, common case.
  for i in os.environ['PATH'].split(os.pathsep):
    if i.rstrip(os.sep).endswith('depot_tools'):
      if directory_really_is_depot_tools(i):
        sys.path.insert(0, i.rstrip(os.sep))
        return i
  # Rare case, it's not even in PATH, look upward up to root.
  root_dir = os.path.dirname(os.path.abspath(__file__))
  previous_dir = os.path.abspath(__file__)
  while root_dir and root_dir != previous_dir:
    if directory_really_is_depot_tools(os.path.join(root_dir, 'depot_tools')):
      i = os.path.join(root_dir, 'depot_tools')
      sys.path.insert(0, i)
      return i
    previous_dir = root_dir
    root_dir = os.path.dirname(root_dir)
  print >> sys.stderr, 'Failed to find depot_tools'
  return None

add_depot_tools_to_path()

# pylint: disable=W0611
import breakpad
