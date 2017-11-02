import unittest, uuid
from nixie.backend import Backend

class BackendTestCase(unittest.TestCase):

  regexp = '[a-f0-9]{32}'

  def setUp(self):
    self.be = Backend()
    self.key = self.be.new()

  def test_new(self):
    self.assertRegexpMatches(self.key, self.regexp)

  def test_read(self):
    self.assertEqual(self.be[self.key], 0)

  def test_update(self):
    self.be[self.key] = 12
    self.assertEqual(self.be[self.key], 12)
    self.be[self.key] = 24
    self.assertEqual(self.be[self.key], 24)

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
