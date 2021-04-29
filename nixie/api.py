import nixie.backend as backend

class Nixie:
  """Core API library"""

  def __init__(self):
    self.storage = backend.Backend()

  """CRUD"""
  def create(self, start=0, step=1, name=None, description=None):
    key = self.storage.new(start, step)
    if name is not None:
      self.storage.counter(key).name = name
    if description is not None:
      self.storage.counter(key).description = description
    return key

  def read(self, key):
    if not key in self.storage:
      raise KeyError('Unknown key {}'.format(key))
    return self.storage[key]

  def update(self, key, value):
    self.__validate_key_value(key, value)
    self.storage[key] = int(value)
    return self.storage[key]

  def delete(self, key):
    self.__validate_key_value(key, 0)
    del self.storage[key]
    return True

  """extra"""
  def exists(self, key):
    return key in self.storage

  def list(self):
    return self.storage.keys()

  def next(self, key):
    self.__validate_key(key)
    i = iter(self.storage.counter(key))
    next(i)
    return self.storage[key]

  def read_meta(self, key):
    self.__validate_key(key)
    c = self.storage.counter(key)
    return {
      "step": c.step,
      "name": c.name,
      "description": c.description
    }

  def update_meta(self, key, step=None, name=None, description=None):
    self.__validate_key(key)
    c = self.storage.counter(key)
    if isinstance(step, int) and step != c.step:
      c.step = step
    if name is not None and name != c.name:
      c.name = name
    if description is not None and description != c.name:
      c.description = description
    return True

  def __validate_key(self, key):
    if not key in self.storage:
      raise KeyError('Unknown key {}'.format(key))

  def __validate_key_value(self, key, value):
    if not key in self.storage:
      raise KeyError('Unknown key {}'.format(key))
    if (isinstance(value, int)
        or value.isdigit()
        or (value[0] in ['-', '+'] and value[1:].isdigit())):
      return True
    else:
      raise ValueError('Invalid value {}'.format(value))


class KeyError(Exception):
  """Custom error on missing key"""

  def __init__(self, value):
    self.value = value

  def __str__(self):
    return self.value
