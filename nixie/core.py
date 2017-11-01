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
    if not key in self.storage:
      raise ValueError('Unknown key')
    if not isinstance(value, (int, long)):
      raise ValueError('Invalid value')
    self.storage[key] += int(value)
    return self.storage[key]

  def delete(self, key):
    if not key in self.storage:
      raise ValueError('Unknown key')
    del self.storage[key]
    return True

  """additional"""
  def exists(self, key):
    return key in self.storage

  def list(self):
    return self.storage.keys()
