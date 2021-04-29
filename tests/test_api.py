import unittest
from nixie.api import Nixie, KeyError

class APITestCase(unittest.TestCase):

  regexp = r'\w{21}'

  def setUp(self):
    self.nx = Nixie()
    self.key1 = self.nx.create()
    self.key2 = self.nx.create()

  def test_create(self):
    self.assertRegex(self.key1, self.regexp)
    self.assertRegex(self.key2, self.regexp)
    self.assertNotEqual(self.key1, self.key2)

  def test_read(self):
    self.assertEqual(self.nx.read(self.key1), 0)
    self.assertEqual(self.nx.read(self.key2), 0)

  def test_read_missing(self):
    with self.assertRaises(KeyError):
      self.nx.read('missing')

  def test_update(self):
    self.assertEqual(self.nx.read(self.key1), 0)
    self.assertEqual(self.nx.update(self.key1, 4), 4)
    self.assertEqual(self.nx.update(self.key1, 8), 8)
    self.assertEqual(self.nx.read(self.key2), 0)
    self.assertEqual(self.nx.update(self.key2, 5), 5)
    self.assertEqual(self.nx.update(self.key2, -10), -10)

  def test_update_missing(self):
    with self.assertRaises(KeyError):
      self.nx.update('missing', 5)

  def test_update_invalid(self):
    with self.assertRaises(ValueError):
      self.nx.update(self.key1, 'boom')

  def test_delete(self):
    self.assertTrue(self.nx.delete(self.key1))
    self.assertFalse(self.nx.exists(self.key1))
    self.assertTrue(self.nx.exists(self.key2))
    self.assertTrue(self.nx.delete(self.key2))
    self.assertFalse(self.nx.exists(self.key2))

  def test_delete_missing(self):
    with self.assertRaises(KeyError):
      self.nx.delete('missing')

  def test_list(self):
    self.nx.create()
    self.nx.create()
    for key in self.nx.list():
      self.assertRegex(key, self.regexp)

  def test_exists(self):
    self.assertTrue(self.nx.exists(self.key1))
    self.assertTrue(self.nx.exists(self.key2))
    self.assertFalse(self.nx.exists('missing'))

  def test_next(self):
    self.assertEqual(self.nx.next(self.key1), 1)
    self.assertEqual(self.nx.next(self.key1), 2)
    self.assertEqual(self.nx.next(self.key1), 3)
    self.assertEqual(self.nx.read(self.key2), 0)
    self.assertEqual(self.nx.next(self.key2), 1)
    self.assertEqual(self.nx.read(self.key2), 1)
