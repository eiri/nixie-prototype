"""
Dict storage backend
"""

class Backend(dict):

  def __init__(self, *arg, **kwarg):
    super(Backend, self).__init__(*arg, **kwarg)

  def get(self, key):
    return int(self[key]) if key in self else None

  def set(self, key, value):
    self[key] = int(value)
    return True

  def remove(self, key):
    if key in self:
      del self[key]
    return True

  def has(self, key):
    return key in self
