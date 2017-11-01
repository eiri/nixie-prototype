"""
Init file storage plugin
"""

import copy, ConfigParser

__storage = ConfigParser.RawConfigParser()
__storage.add_section('main')

def get(key):
  if __storage.has_option('main', key):
    return __storage.getint('main', key)
  else:
    return None

def set(key, value):
  __storage.set('main', key, str(value))
  return True

def remove(key):
  if __storage.has_option('main', key):
    __storage.remove_option('main', key)
  return True

def has(key):
  return __storage.has_option('main', key)

def as_dict():
  return {key: int(value) for (key, value) in __storage.items('main')}

def as_str():
  return hex(id(__storage))