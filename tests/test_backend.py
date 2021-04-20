import unittest, time
from nixie.backend import Backend

class BackendTestCase(unittest.TestCase):

  regexp = '\w{21}'

  def setUp(self):
    self.be = Backend()
    self.key = self.be.new()

  def test_new(self):
    self.assertRegexpMatches(self.key, self.regexp)

  def test_read(self):
    self.assertEqual(self.be[self.key], 0)

  def test_get(self):
    (ts, val) = self.be.get(self.key)
    now = int(time.time())
    self.assertEqual(ts, now)
    self.assertEqual(val, 0)

  def test_update(self):
    self.be[self.key] = 12
    self.assertEqual(self.be[self.key], 12)
    self.be[self.key] = 24
    self.assertEqual(self.be[self.key], 24)

  def test_update_timestamped(self):
    self.be[self.key] = 12
    (ts1, val1) = self.be.get(self.key)
    self.assertLessEqual(ts1, int(time.time()))
    self.assertEqual(val1, 12)
    time.sleep(1)
    self.be[self.key] = 24
    (ts2, val2) = self.be.get(self.key)
    self.assertGreater(ts2, ts1)
    self.assertEqual(val2, 24)

  def test_all(self):
    self.be[self.key] = 1
    self.be[self.key] = 2
    now = int(time.time())
    trb = self.be.all(self.key)
    self.assertEqual(trb, [(now, 0), (now, 1), (now, 2)])

  def test_in(self):
    self.assertTrue(self.key in self.be)

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
