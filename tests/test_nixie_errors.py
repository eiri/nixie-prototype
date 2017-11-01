import unittest, uuid
from nixie.core import Nixie

class NixieErrorsTestCase(unittest.TestCase):

  def test_read_missing(self):
    nx = Nixie()
    value = nx.read('missing_counter')
    self.assertIsNone(value)

  def test_update_missing(self):
    nx = Nixie()
    value = nx.update('missing_counter')
    self.assertIsNone(value)

  def test_update_with_wrong_value(self):
    nx = Nixie()
    key = nx.create()
    value = nx.update(key, '5')
    self.assertIsNone(value)

  def test_delete_missing(self):
    nx = Nixie()
    counter_name = 'missing_counter'
    delete_result = nx.delete(counter_name)
    exists_after = nx.exists(counter_name)
    self.assertIsNone(delete_result)
    self.assertFalse(exists_after)
