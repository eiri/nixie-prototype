import unittest, time
from nixie.backend import TimedRingBuffer

class RingBufferTestCase(unittest.TestCase):

  regexp = '[a-f0-9]{32}'

  def setUp(self):
    self.trb = TimedRingBuffer(3)

  def test_read_new(self):
    self.assertIsNone(self.trb.get())

  def test_append(self):
    self.assertIsNone(self.trb.append(1))
    self.assertEqual(len(self.trb), 1)

  def test_get(self):
    now = int(time.time())
    self.trb.append(1)
    self.assertEqual(self.trb.get(), (now, 1))
    self.trb.append(2)
    self.assertEqual(self.trb.get(), (now, 2))
    self.trb.append(3)
    self.assertEqual(self.trb.get(), (now, 3))
    self.trb.append(4)
    self.assertEqual(self.trb.get(), (now, 4))
    self.trb.append(5)
    self.assertEqual(self.trb.get(), (now, 5))

  def test_all(self):
    now = int(time.time())
    self.trb.append(1)
    self.assertEqual(self.trb.all(), [(now, 1)])
    self.trb.append(2)
    self.assertEqual(self.trb.all(), [(now, 1), (now, 2)])
    self.trb.append(3)
    self.assertEqual(self.trb.all(), [(now, 1), (now, 2), (now, 3)])
    self.trb.append(4)
    self.assertEqual(self.trb.all(), [(now, 2), (now, 3), (now, 4)])
    self.trb.append(5)
    self.assertEqual(self.trb.all(), [(now, 3), (now, 4), (now, 5)])

  def test_length(self):
    self.assertEqual(len(self.trb), 0)
    for i in range(9):
      self.trb.append(i)
    self.assertEqual(len(self.trb), 3)
