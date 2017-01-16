import unittest, uuid
from nixie import nixie

class NixieTestCase(unittest.TestCase):

  regexp = '[a-f0-9]{32}'

  def test_create_default(self):
    key = nixie.create()
    self.assertRegexpMatches(key, self.regexp)

  def test_create_with_value(self):
    key = nixie.create(42)
    self.assertRegexpMatches(key, self.regexp)

  def test_create_with_bad_value(self):
    key = nixie.create('42')
    self.assertIsNone(key)

  def test_create_and_read_default(self):
    key = nixie.create()
    value = nixie.read(key)
    self.assertEqual(value, 0)

  def test_create_and_read_with_value(self):
    counter_value = 42
    key = nixie.create(counter_value)
    value = nixie.read(key)
    self.assertEqual(value, counter_value)

  def test_read_missing(self):
    value = nixie.read('missing_counter')
    self.assertIsNone(value)

  def test_list(self):
    counters = nixie.list()
    self.assertIsInstance(counters, dict)
    [self.assertRegexpMatches(k, self.regexp) for k in counters.keys()]
    [self.assertIsInstance(v, (int, long)) for v in counters.values()]

  def test_update_default(self):
    key = nixie.create()
    value = nixie.update(key)
    self.assertEqual(value, 1)
    value = nixie.update(key)
    self.assertEqual(value, 2)

  def test_update_with_value(self):
    key = nixie.create(1)
    value = nixie.update(key, 4)
    self.assertEqual(value, 5)
    value = nixie.update(key, 12)
    self.assertEqual(value, 17)

  def test_update_with_negative_value(self):
    key = nixie.create(10)
    value = nixie.update(key, -5)
    self.assertEqual(value, 5)

  def test_update_missing(self):
    value = nixie.update('missing_counter')
    self.assertIsNone(value)

  def test_update_with_wrong_value(self):
    key = nixie.create()
    value = nixie.update(key, '5')
    self.assertIsNone(value)

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

  def test_delete_missing(self):
    counter_name = 'missing_counter'
    delete_result = nixie.delete(counter_name)
    exists_after = nixie.exists(counter_name)
    self.assertIsNone(delete_result)
    self.assertFalse(exists_after)
