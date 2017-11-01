import unittest, uuid
from nixie import nixie

class NixieErrorsTestCase(unittest.TestCase):

  def test_read_missing(self):
    value = nixie.read('missing_counter')
    self.assertIsNone(value)

  def test_update_missing(self):
    value = nixie.update('missing_counter')
    self.assertIsNone(value)

  def test_update_with_wrong_value(self):
    key = nixie.create()
    value = nixie.update(key, '5')
    self.assertIsNone(value)

  def test_delete_missing(self):
    counter_name = 'missing_counter'
    delete_result = nixie.delete(counter_name)
    exists_after = nixie.exists(counter_name)
    self.assertIsNone(delete_result)
    self.assertFalse(exists_after)
