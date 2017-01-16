"""
Main API library
"""

import copy, uuid

storage = {}

def create(value=0):
  if not isinstance(value, (int, long)):
    return None
  key = uuid.uuid4().hex
  if key not in storage:
    storage[key] = value
  return key

def exists(key):
  return key in storage

def list():
  return copy.copy(storage)

def read(key):
  if key in storage:
    return storage[key]
  else:
    return None

def update(key, value=1):
  if key in storage and isinstance(value, (int, long)):
    storage[key] += value
    return storage[key]
  else:
    return None

def delete(key):
  if key in storage:
    del storage[key]
    return True
  else:
    return None
