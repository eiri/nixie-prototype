"""
Main API library
"""

import uuid, collections, backend

class Nixie:

  def __init__(self):
    self.storage = backend.Backend()

  def create(self):
    key = uuid.uuid4().hex
    if self.storage.has(key):
      raise ValueError('Existing key')
    self.storage.set(key, 0)
    return key

  def exists(self, key):
    return self.storage.has(key)

  def list(self):
    return self.storage.keys()

  def read(self, key):
    if self.storage.has(key):
      return self.storage.get(key)
    else:
      return None

  def update(self, key, value=1):
    if not self.storage.has(key):
      raise ValueError('Unknown key')
    if not isinstance(value, (int, long)):
      raise ValueError('Invalid value')
    new_value = self.storage.get(key) + value
    self.storage.set(key, new_value)
    return new_value

  def delete(self, key):
    if not self.storage.has(key):
      raise ValueError('Unknown key')
    self.storage.remove(key)
    return True
