"""
Dict storage backend
"""

class Backend():

  def __init__(self):
    self.storage = {}

  def get(self, key):
    return int(self.storage[key]) if key in self.storage else None

  def set(self, key, value):
    self.storage[key] = int(value)
    return True

  def remove(self, key):
    if key in self.storage:
      del self.storage[key]
    return True

  def has(self, key):
    return key in self.storage

  def keys(self):
    return self.storage.keys()
