"""
Main API library
"""

import os, uuid, imp, functools

cfg = {
  'frontend': None,
  'backend': 'backend'
}

__backend = None

def with_storage(func=None, debug=False):
  if func is None:
    return functools.partial(with_storage, debug=debug)
  @functools.wraps(func)
  def wrapper(*args, **kwargs):
    global __backend
    if __backend is None:
      here = os.path.dirname(os.path.realpath(__file__))
      module_info = imp.find_module(cfg['backend'], [here])
      __backend = imp.load_module('backend', *module_info)
    if debug:
      print 'func {}, backend <{}>\n'.format(func.__name__, __backend.as_str())
    func_with_storage = functools.partial(func, storage=__backend)
    return func_with_storage(*args, **kwargs)
  return wrapper

@with_storage
def create(value=0, storage=None):
  if not isinstance(value, (int, long)):
    return None
  key = uuid.uuid4().hex
  if not storage.has(key):
    storage.set(key, value)
  return key

@with_storage
def exists(key, storage=None):
  return storage.has(key)

@with_storage
def list(storage=None):
  return storage.as_dict()

@with_storage
def read(key, storage=None):
  if storage.has(key):
    return storage.get(key)
  else:
    return None

@with_storage
def update(key, value=1, storage=None):
  if storage.has(key) and isinstance(value, (int, long)):
    new_value = storage.get(key) + value
    storage.set(key, new_value)
    return new_value
  else:
    return None

@with_storage
def delete(key, storage=None):
  if storage.has(key):
    storage.remove(key)
    return True
  else:
    return None
