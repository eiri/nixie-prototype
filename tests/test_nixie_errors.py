import unittest, uuid
from nixie.core import Nixie

class NixieErrorsTestCase(unittest.TestCase):

  def test_read_missing(self):
    nx = Nixie()
    self.assertIsNone(nx.read('missing'))

  def test_update_missing(self):
    nx = Nixie()
    with self.assertRaises(KeyError):
      nx.update('missing')

  def test_update_with_wrong_value(self):
    nx = Nixie()
    key = nx.create()
    with self.assertRaises(ValueError):
      nx.update(key, 'a')

  def test_delete_missing(self):
    nx = Nixie()
    with self.assertRaises(KeyError):
      nx.delete('missing')
