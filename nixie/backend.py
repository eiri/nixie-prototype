import uuid, collections, time

class Backend(collections.MutableMapping):
  """Dict-like storage for counters"""

  def new(self):
    key = uuid.uuid4().hex
    if key in self.store:
      raise ValueError('key collision')
    self.__setitem__(key, 0)
    return key

  def get(self, key):
    return self.store[key]

  def __init__(self):
    self.store = dict()

  def __getitem__(self, key):
    (_, val) = self.store[key]
    return val

  def __setitem__(self, key, value):
    ts = int(time.time())
    val = int(value)
    self.store[key] = (ts, val)
    return val

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
