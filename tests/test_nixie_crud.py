import unittest
from nixie.core import Nixie

class NixieCRUDTestCase(unittest.TestCase):

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

  def test_update(self):
    nx = Nixie()
    key1 = nx.create()
    key2 = nx.create()
    self.assertEqual(nx.update(key1), 1)
    self.assertEqual(nx.update(key1), 2)
    self.assertEqual(nx.read(key2), 0)
    self.assertEqual(nx.update(key2), 1)
    self.assertEqual(nx.update(key2), 2)
    self.assertEqual(nx.update(key2), 3)
    self.assertEqual(nx.read(key1), 2)

  def test_update_with_value(self):
    nx = Nixie()
    key1 = nx.create()
    key2 = nx.create()
    self.assertEqual(nx.update(key1, 4), 4)
    self.assertEqual(nx.update(key1, 8), 12)
    self.assertEqual(nx.read(key2), 0)
    self.assertEqual(nx.update(key2, 5), 5)
    self.assertEqual(nx.update(key2, 10), 15)
    self.assertEqual(nx.read(key1), 12)

  def test_update_with_negative_value(self):
    nx = Nixie()
    key = nx.create()
    self.assertEqual(nx.update(key, -5), -5)

  def test_delete(self):
    nx = Nixie()
    key1 = nx.create()
    key2 = nx.create()
    self.assertTrue(nx.delete(key1))
    self.assertFalse(nx.exists(key1))
    self.assertTrue(nx.exists(key2))
    self.assertTrue(nx.delete(key2))
    self.assertFalse(nx.exists(key2))
