import backend

class Nixie:
  """Core API library"""

  def __init__(self):
    self.storage = backend.Backend()

  """CRUD"""
  def create(self):
    key = self.storage.new()
    return key

  def read(self, key):
    if key in self.storage:
      return self.storage[key]
    else:
      return None

  def update(self, key, value=1):
    self.__validate_key_value(key, value)
    self.storage[key] += int(value)
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

  def put(self, key, value):
    self.__validate_key_value(key, value)
    self.storage[key] = int(value)
    return self.storage[key]

  def incr(self, key):
    return self.update(key)

  def decr(self, key):
    return self.update(key, -1)

  def __validate_key_value(self, key, value):
    if not key in self.storage:
      raise KeyError('Unknown key {}'.format(key))
    if (isinstance(value, (int, long))
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
      return repr(self.value)
