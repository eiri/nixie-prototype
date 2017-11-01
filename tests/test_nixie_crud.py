import unittest, uuid
from nixie import nixie

class NixieCRUDTestCase(unittest.TestCase):

  regexp = '[a-f0-9]{32}'

  def test_create_default(self):
    key = nixie.create()
    self.assertRegexpMatches(key, self.regexp)

  def test_create_and_read(self):
    key = nixie.create()
    value = nixie.read(key)
    self.assertEqual(value, 0)

  def test_list(self):
    keys = nixie.list()
    self.assertIsInstance(keys, list)
    [self.assertRegexpMatches(key, self.regexp) for key in keys]

  def test_update(self):
    key = nixie.create()
    value = nixie.update(key)
    self.assertEqual(value, 1)
    value = nixie.update(key)
    self.assertEqual(value, 2)

  def test_update_with_value(self):
    key = nixie.create()
    value = nixie.update(key, 4)
    self.assertEqual(value, 4)
    value = nixie.update(key, 12)
    self.assertEqual(value, 16)

  def test_update_with_negative_value(self):
    key = nixie.create()
    value = nixie.update(key, -5)
    self.assertEqual(value, -5)

  def test_exists(self):
    key = nixie.create()
    exists = nixie.exists(key)
    self.assertTrue(exists)

  def test_exists_missing(self):
    exists = nixie.exists('missing_counter')
    self.assertFalse(exists)

  def test_delete(self):
    key = nixie.create()
    exists = nixie.exists(key)
    self.assertTrue(exists)
    delete_result = nixie.delete(key)
    exists_after = nixie.exists(key)
    self.assertTrue(delete_result)
    self.assertFalse(exists_after)
