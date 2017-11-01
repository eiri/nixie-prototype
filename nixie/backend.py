import collections

class Backend(collections.MutableMapping):
  """Dict-like storage for counters"""

  def __init__(self):
    self.store = dict()

  def __getitem__(self, key):
    return self.store[key]

  def __setitem__(self, key, value):
    self.store[key] = int(value)

  def __delitem__(self, key):
    del self.store[key]

  def __iter__(self):
    return iter(self.store)

  def __len__(self):
    return len(self.store)

  def __repr__(self):
    return 'nixie.Backend of {}'.format(hex(id(self)))

  def __str__(self):
    return 'nixie.Backend<id: {}; length: {}>'.format(hex(id(self)), len(self))
