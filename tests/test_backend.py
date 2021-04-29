import unittest, time
from nixie.backend import Counter, TimedRingBuffer, Backend


class RingBufferTestCase(unittest.TestCase):

  empty = TimedRingBuffer(3)
  counter = TimedRingBuffer(3)

  def test_empty_counter(self):
    self.assertIsNone(self.empty)

  def test_set_counter(self):
    # now = int(time.time())
    for i in range(1, 6):
      self.counter = i
      self.assertEqual(self.counter, i)

  def test_str_len(self):
    trb = TimedRingBuffer(3)
    self.assertTrue(str(trb).startswith('nixie.TimedRingBuffer'))
    self.assertTrue('length: 0' in str(trb))
    # add one
    trb.__set__(None, 1)
    self.assertTrue('length: 1' in str(trb))
    self.assertEqual(len(trb), 1)
    # make full cicrle
    for i in range(1, 6):
      trb.__set__(None, i)
    self.assertTrue('length: 3' in str(trb))
    self.assertEqual(len(trb), 3)

  def test_repr(self):
    trb = TimedRingBuffer(3)
    self.assertTrue(repr(trb).startswith('nixie.TimedRingBuffer'))


class CounterTestCase(unittest.TestCase):

  def setUp(self):
    self.c = Counter()

  def test_empty_counter(self):
    self.assertEqual(self.c.value, 0)

  def test_set_counter(self):
    for i in range(1, 6):
      self.c.value = i
      self.assertEqual(self.c.value, i)

  def test_increase_counter(self):
    for i in range(1, 6):
      self.c.value = i
      v = self.c + 2
      self.assertEqual(self.c.value, i)
      self.assertEqual(v, i + 2)

  def test_decrease_counter(self):
    for i in range(1, 6):
      self.c.value = i
      v = self.c - 2
      self.assertEqual(self.c.value, i)
      self.assertEqual(v, i - 2)

  def test_reverse_increase_counter(self):
    for i in range(1, 6):
      self.c.value = i
      v = 2 + self.c
      self.assertEqual(self.c.value, i)
      self.assertEqual(v, 2 + i)

  def test_reverse_decrease_counter(self):
    for i in range(1, 6):
      self.c.value = i
      v = 2 - self.c
      self.assertEqual(self.c.value, i)
      self.assertEqual(v, 2 - i)

  def test_aug_increase_counter(self):
    self.c.value = 0
    for i in range(1, 6):
      self.c.value += 2
      self.assertEqual(self.c.value, i * 2)

  def test_aug_decrease_counter(self):
    self.c.value = 0
    for i in range(1, 6):
      self.c.value -= 2
      self.assertEqual(self.c.value, - (i * 2))

  def test_iter_default_counter(self):
    self.c.value = 0
    i = iter(self.c)
    self.assertEqual(next(i), 0)
    self.assertEqual(next(i), 1)
    self.assertEqual(next(i), 2)

  def test_iter_counter(self):
    for tc in ((1, 1), (2, 3)):
      (start, step) = tc
      self.c = Counter(start, step)
      i = iter(self.c)
      self.assertEqual(next(i), start)
      self.assertEqual(next(i), start + step)
      self.assertEqual(next(i), start + 2 * step)

  def test_cycle_counter(self):
    self.c.step = 2
    self.c.value = 0
    for i in self.c:
      if i > 10:
        break
      self.assertEqual(self.c.value, i + self.c.step)

  def test_meta(self):
    c = Counter(2, 3, 'custom name', 'custom description')
    self.assertEqual(c.step, 3)
    self.assertEqual(c.name, 'custom name')
    self.assertEqual(c.description, 'custom description')

  def test_str(self):
    self.assertTrue(str(self.c).startswith('nixie.Counter'))
    self.assertTrue('value: 0' in str(self.c))
    self.c.value = 12
    self.assertTrue('value: 12' in str(self.c))

  def test_repr(self):
    self.assertTrue(repr(self.c).startswith('nixie.Counter'))


class BackendTestCase(unittest.TestCase):

  regexp = r'\w{21}'

  def setUp(self):
    self.be = Backend()
    self.key = self.be.new()

  def test_new(self):
    self.assertRegex(self.key, self.regexp)

  def test_in(self):
    self.assertTrue(self.key in self.be)

  def test_read(self):
    self.assertEqual(self.be[self.key], 0)

  def test_update(self):
    self.be[self.key] = 12
    self.assertEqual(self.be[self.key], 12)
    self.be[self.key] = 24
    self.assertEqual(self.be[self.key], 24)

  def test_delete(self):
    self.assertTrue(self.key in self.be)
    del self.be[self.key]
    self.assertFalse(self.key in self.be)

  def test_len(self):
    self.assertEqual(len(self.be), 1)
    self.be.new()
    self.be.new()
    self.assertEqual(len(self.be), 3)

  def test_str(self):
    self.assertTrue(str(self.be).startswith('nixie.Backend'))

  def test_repr(self):
    self.assertTrue(repr(self.be).startswith('nixie.Backend'))
