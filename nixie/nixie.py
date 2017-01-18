"""
Main API library
"""

import copy, uuid, imp

backend = None

def __get_storage():
  global backend
  if backend is None:
    module_info = imp.find_module('backend', ['./nixie'])
    backend = imp.load_module('backend', *module_info)
  storage = backend.get_storage()
  # print 'storage at <{0}>'.format(hex(id(storage)))
  return storage

def create(value=0):
  storage = __get_storage()
  if not isinstance(value, (int, long)):
    return None
  key = uuid.uuid4().hex
  if key not in storage:
    storage[key] = value
  return key

def exists(key):
  storage = __get_storage()
  return key in storage

def list():
  storage = __get_storage()
  return copy.copy(storage)

def read(key):
  storage = __get_storage()
  if key in storage:
    return storage[key]
  else:
    return None

def update(key, value=1):
  storage = __get_storage()
  if key in storage and isinstance(value, (int, long)):
    storage[key] += value
    return storage[key]
  else:
    return None

def delete(key):
  storage = __get_storage()
  if key in storage:
    del storage[key]
    return True
  else:
    return None
