"""
Dict storage plugin
"""

__storage = {}

def get(key):
  return int(__storage[key]) if key in __storage else None

def set(key, value):
  __storage[key] = int(value)
  return True

def remove(key):
  if key in __storage:
    del __storage[key]
  return True

def has(key):
  return key in __storage

def keys():
  return __storage.keys()

def as_str():
  return hex(id(__storage))
