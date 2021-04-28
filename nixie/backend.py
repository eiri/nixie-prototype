import collections, time

from collections.abc import MutableMapping
from nanoid import generate

class TimedRingBuffer:
  """Circular buffer with timestamped entries"""

  def __init__(self, maxlen=5):
    self.q = collections.deque(maxlen=maxlen)

  def __get__(self, instance, owner):
    if len(self.q) == 0:
      return None
    else:
      (_, v) = self.q[-1]
      return v

  def __set__(self, instance, value):
    ts = int(time.time())
    val = int(value)
    self.q.append((ts, val))

  def __len__(self):
    return len(self.q)

  def __repr__(self):
    return f'nixie.TimedRingBuffer of {hex(id(self))}'

  def __str__(self):
    return f'nixie.TimedRingBuffer<id: {hex(id(self))}; length: {len(self)}>'


class Counter:
  """Class representing a counter"""

  def __init__(self, start=0, step=1):
    Counter.value = TimedRingBuffer()
    Counter.value = start
    self.step = step

  def __add__(self, other):
    return self.value + other

  def __sub__(self, other):
    return self.value - other

  def __radd__(self, other):
    return other + self.value

  def __rsub__(self, other):
    return other - self.value

  def __iter__(self):
    return self

  def __next__(self):
    value = self.value
    self.value += self.step
    return value

  def __repr__(self):
    return f'nixie.Counter of {hex(id(self))}'

  def __str__(self):
    return f'nixie.Counter<id: {hex(id(self))}; value: {self.value}>'


class Backend(MutableMapping):
  """Dict-like storage for counters"""

  def __init__(self):
    self.store = dict()

  def new(self, start=0, step=1):
    key = generate('346789ABCDEFGHJKLMNPQRTUVWXYabcdefghijkmnpqrtwxyz')
    if key in self.store:
      raise ValueError('key collision')
    self.store[key] = Counter(start, step)
    return key

  def counter(self, key):
    return self.store[key]

  def __getitem__(self, key):
    return self.store[key].value

  def __setitem__(self, key, value):
    self.store[key].value = value
    return value

  def __delitem__(self, key):
    del self.store[key]

  def __iter__(self):
    return iter(self.store)

  def __len__(self):
    return len(self.store)

  def __repr__(self):
    return f'nixie.Backend of {hex(id(self))}'

  def __str__(self):
    return f'nixie.Backend<id: {hex(id(self))}; length: {len(self)}>'
