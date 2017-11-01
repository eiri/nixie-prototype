"""
Main API library
"""

import uuid, backend

class Nixie:

  def __init__(self):
    self.storage = backend.Backend()

  def create(self):
    key = uuid.uuid4().hex
    if not self.storage.has(key):
      self.storage.set(key, 0)
      return key
    else:
      return None

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
    if self.storage.has(key) and isinstance(value, (int, long)):
      new_value = self.storage.get(key) + value
      self.storage.set(key, new_value)
      return new_value
    else:
      return None

  def delete(self, key):
    if self.storage.has(key):
      self.storage.remove(key)
      return True
    else:
      return None
