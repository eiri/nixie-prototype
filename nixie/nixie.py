"""
Main API library
"""

import copy, uuid, imp, functools

backend = None

def with_storage(func=None, debug=False):
  if func is None:
    return functools.partial(with_storage, debug=debug)
  @functools.wraps(func)
  def wrapper(*args, **kwargs):
    global backend
    if backend is None:
      module_info = imp.find_module('backend', ['./nixie'])
      backend = imp.load_module('backend', *module_info)
    storage = backend.get_storage()
    if debug:
      print 'func {}, storage <{}>\n'.format(func.__name__, hex(id(storage)))
    func_with_storage = functools.partial(func, storage=storage)
    return func_with_storage(*args, **kwargs)
  return wrapper

@with_storage
def create(value=0, storage=None):
  if not isinstance(value, (int, long)):
    return None
  key = uuid.uuid4().hex
  if key not in storage:
    storage[key] = value
  return key

@with_storage
def exists(key, storage=None):
  return key in storage

@with_storage
def list(storage=None):
  return copy.copy(storage)

@with_storage
def read(key, storage=None):
  if key in storage:
    return storage[key]
  else:
    return None

@with_storage
def update(key, value=1, storage=None):
  if key in storage and isinstance(value, (int, long)):
    storage[key] += value
    return storage[key]
  else:
    return None

@with_storage
def delete(key, storage=None):
  if key in storage:
    del storage[key]
    return True
  else:
    return None
