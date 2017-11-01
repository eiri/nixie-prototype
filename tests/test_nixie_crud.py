import unittest, uuid
from nixie.core import Nixie

class NixieCRUDTestCase(unittest.TestCase):

  regexp = '[a-f0-9]{32}'

  def test_create_default(self):
    nx = Nixie()
    key = nx.create()
    self.assertRegexpMatches(key, self.regexp)

  def test_create_and_read(self):
    nx = Nixie()
    key = nx.create()
    value = nx.read(key)
    self.assertEqual(value, 0)

  def test_list(self):
    nx = Nixie()
    keys = nx.list()
    self.assertIsInstance(keys, list)
    [self.assertRegexpMatches(key, self.regexp) for key in keys]

  def test_update(self):
    nx = Nixie()
    key = nx.create()
    value = nx.update(key)
    self.assertEqual(value, 1)
    value = nx.update(key)
    self.assertEqual(value, 2)

  def test_update_with_value(self):
    nx = Nixie()
    key = nx.create()
    value = nx.update(key, 4)
    self.assertEqual(value, 4)
    value = nx.update(key, 12)
    self.assertEqual(value, 16)

  def test_update_with_negative_value(self):
    nx = Nixie()
    key = nx.create()
    value = nx.update(key, -5)
    self.assertEqual(value, -5)

  def test_exists(self):
    nx = Nixie()
    key = nx.create()
    exists = nx.exists(key)
    self.assertTrue(exists)

  def test_exists_missing(self):
    nx = Nixie()
    exists = nx.exists('missing_counter')
    self.assertFalse(exists)

  def test_delete(self):
    nx = Nixie()
    key = nx.create()
    exists = nx.exists(key)
    self.assertTrue(exists)
    delete_result = nx.delete(key)
    exists_after = nx.exists(key)
    self.assertTrue(delete_result)
    self.assertFalse(exists_after)
