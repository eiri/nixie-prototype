import uuid, collections, backend

class Nixie:
  """Core API library"""

  def __init__(self):
    self.storage = backend.Backend()

  """CRUD"""
  def create(self):
    key = uuid.uuid4().hex
    if key in self.storage:
      raise ValueError('Existing key')
    self.storage[key] = 0
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
    new_value = self.storage[key] + int(value)
    self.storage[key] = new_value
    return new_value

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
