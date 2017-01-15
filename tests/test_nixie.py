import unittest, uuid
from nixie import nixie

class NixieTestCase(unittest.TestCase):

  def test_00_config(self):
    cfg = nixie.config()
    self.assertIsInstance(cfg, dict)

  def test_01_create_default(self):
    regexp = '[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}'
    '-?[89ab][a-f0-9]{3}-?[a-f0-9]{12}'
    key = nixie.create()
    self.assertRegexpMatches(key, regexp)

  def test_02_create_with_key(self):
    counter_name = 'counter'
    key = nixie.create(counter_name)
    self.assertEqual(key, counter_name)

  def test_03_create_with_key_and_value(self):
    counter_name = 'counter_42'
    counter_value = 42
    key = nixie.create(counter_name, counter_value)
    self.assertEqual(key, counter_name)

  def test_04_create_with_key_and_wrong_value(self):
    counter_name = 'bad_counter'
    counter_value = 'str'
    key = nixie.create(counter_name, counter_value)
    self.assertIsNone(key)

  def test_05_create_and_read_default(self):
    key = nixie.create()
    value = nixie.read(key)
    self.assertEqual(value, 0)

  def test_06_create_and_read_with_value(self):
    counter_value = 42
    key = nixie.create(value=counter_value)
    value = nixie.read(key)
    self.assertEqual(value, counter_value)

  def test_07_read_named(self):
    counter_name = 'counter'
    value = nixie.read(counter_name)
    self.assertEqual(value, 0)

  def test_08_read_named_with_value(self):
    counter_name = 'counter_42'
    counter_value = 42
    value = nixie.read(counter_name)
    self.assertEqual(value, counter_value)

  def test_09_create_existing(self):
    counter_name = 'counter_42'
    counter_value = 42
    counter_new_value = 9001
    key = nixie.create(counter_name, counter_new_value)
    value = nixie.read(counter_name)
    self.assertEqual(key, counter_name)
    self.assertEqual(value, counter_value)

  def test_10_read_missing(self):
    counter_name = 'missing_counter'
    value = nixie.read(counter_name)
    self.assertIsNone(value)

  def test_11_list(self):
    counters = nixie.list()
    counter_name = 'counter'
    counter_value = 0
    counter_name_42 = 'counter_42'
    counter_value_42 = 42
    missing_counter_name = 'missing_counter'
    self.assertEqual(len(counters), 5)
    self.assertIn(counter_name, counters)
    self.assertIn(counter_name_42, counters)
    self.assertNotIn(missing_counter_name, counters)
    self.assertEqual(counters[counter_name], counter_value)
    self.assertEqual(counters[counter_name_42], counter_value_42)

  def test_12_update_default(self):
    counter_name = 'counter'
    counter_value = 0
    new_value = nixie.update(counter_name)
    self.assertEqual(new_value, counter_value + 1)

  def test_13_update_with_value(self):
    counter_name = 'counter'
    counter_value = 1
    new_value = nixie.update(counter_name, 4)
    self.assertEqual(new_value, counter_value + 4)

  def test_14_update_with_negative_value(self):
    counter_name = 'counter'
    counter_value = 5
    new_value = nixie.update(counter_name, -5)
    self.assertEqual(new_value, counter_value - 5)

  def test_15_update_missing(self):
    counter_name = 'missing_counter'
    change_result = nixie.update(counter_name)
    self.assertIsNone(change_result)

  def test_16_update_with_wrong_value(self):
    counter_name = 'counter'
    change_result = nixie.update(counter_name, 'str')
    self.assertIsNone(change_result)

  def test_17_exists(self):
    counter_name = 'counter'
    is_result = nixie.exists(counter_name)
    self.assertTrue(is_result)

  def test_18_exists_missing(self):
    counter_name = 'missing_counter'
    is_result = nixie.exists(counter_name)
    self.assertFalse(is_result)

  def test_19_delete(self):
    counter_name = 'counter'
    delete_result = nixie.delete(counter_name)
    exists_after = nixie.exists(counter_name)
    self.assertTrue(delete_result)
    self.assertFalse(exists_after)

  def test_20_delete_missing(self):
    counter_name = 'missing_counter'
    delete_result = nixie.delete(counter_name)
    exists_after = nixie.exists(counter_name)
    self.assertIsNone(delete_result)
    self.assertFalse(exists_after)
