import unittest
from nixie.core import Nixie

class NixieExtraTestCase(unittest.TestCase):

  regexp = '[a-f0-9]{32}'

  def test_list(self):
    nx = Nixie()
    nx.create()
    nx.create()
    keys = nx.list()
    self.assertIsInstance(keys, list)
    [self.assertRegexpMatches(key, self.regexp) for key in keys]

  def test_exists(self):
    nx = Nixie()
    key1 = nx.create()
    key2 = nx.create()
    self.assertTrue(nx.exists(key1))
    self.assertTrue(nx.exists(key2))
    self.assertFalse(nx.exists('missing_counter'))
