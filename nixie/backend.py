import collections, time

from collections.abc import MutableMapping
from nanoid import generate

class Backend(MutableMapping):
  """Dict-like storage for counters"""

  def __init__(self):
    self.store = dict()

  def new(self, buffer_size=5):
    key = generate('346789ABCDEFGHJKLMNPQRTUVWXYabcdefghijkmnpqrtwxyz')
    if key in self.store:
      raise ValueError('key collision')
    self.store[key] = TimedRingBuffer(buffer_size)
    self.__setitem__(key, 0)
    return key

  def get(self, key):
    val = self.store[key].get()
    return val

  def all(self, key):
    rbuffer = self.store[key].all()
    return rbuffer

  def __getitem__(self, key):
    (_, val) = self.get(key)
    return val

  def __setitem__(self, key, value):
    self.store[key].append(value)
    return value

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


class TimedRingBuffer:
  """Circular buffer with timestamped enties"""

  def __init__(self, maxlen):
    self.data = collections.deque(maxlen=maxlen)

  def append(self, value):
    ts = int(time.time())
    val = int(value)
    self.data.append((ts, val))

  def get(self):
    if len(self.data) == 0:
      return None
    else:
      return self.data[-1]

  def all(self):
    return list(self.data)

  def __len__(self):
    return len(self.data)
