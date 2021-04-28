import unittest
from nixie.api import Nixie, KeyError

class APITestCase(unittest.TestCase):

  regexp = r'\w{21}'

  def test_create(self):
    nx = Nixie()
    key1 = nx.create()
    key2 = nx.create()
    self.assertRegex(key1, self.regexp)
    self.assertRegex(key2, self.regexp)
    self.assertNotEqual(key1, key2)

  def test_read(self):
    nx = Nixie()
    key1 = nx.create()
    key2 = nx.create()
    self.assertEqual(nx.read(key1), 0)
    self.assertEqual(nx.read(key2), 0)

  def test_read_missing(self):
    nx = Nixie()
    with self.assertRaises(KeyError):
      nx.read('missing')

  def test_update(self):
    nx = Nixie()
    key1 = nx.create()
    key2 = nx.create()
    self.assertEqual(nx.read(key1), 0)
    self.assertEqual(nx.update(key1, 4), 4)
    self.assertEqual(nx.update(key1, 8), 8)
    self.assertEqual(nx.read(key2), 0)
    self.assertEqual(nx.update(key2, 5), 5)
    self.assertEqual(nx.update(key2, -10), -10)

  def test_update_missing(self):
    nx = Nixie()
    with self.assertRaises(KeyError):
      nx.update('missing', 5)

  def test_update_invalid(self):
    nx = Nixie()
    key1 = nx.create()
    with self.assertRaises(ValueError):
      nx.update(key1, 'boom')

  def test_delete(self):
    nx = Nixie()
    key1 = nx.create()
    key2 = nx.create()
    self.assertTrue(nx.delete(key1))
    self.assertFalse(nx.exists(key1))
    self.assertTrue(nx.exists(key2))
    self.assertTrue(nx.delete(key2))
    self.assertFalse(nx.exists(key2))

  def test_delete_missing(self):
    nx = Nixie()
    with self.assertRaises(KeyError):
      nx.delete('missing')

  def test_list(self):
    nx = Nixie()
    nx.create()
    nx.create()
    for key in nx.list():
      self.assertRegex(key, self.regexp)

  def test_exists(self):
    nx = Nixie()
    key1 = nx.create()
    key2 = nx.create()
    self.assertTrue(nx.exists(key1))
    self.assertTrue(nx.exists(key2))
    self.assertFalse(nx.exists('missing'))

  def test_next(self):
    nx = Nixie()
    key1 = nx.create()
    key2 = nx.create()
    self.assertEqual(nx.next(key1), 1)
    self.assertEqual(nx.next(key1), 2)
    self.assertEqual(nx.next(key1), 3)
    self.assertEqual(nx.read(key2), 0)
    self.assertEqual(nx.next(key2), 1)
    self.assertEqual(nx.read(key2), 1)
