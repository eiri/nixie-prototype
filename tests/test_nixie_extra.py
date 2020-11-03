import unittest
from nixie.core import Nixie
from collections import KeysView

class NixieExtraTestCase(unittest.TestCase):

  regexp = '[a-f0-9]{32}'

  def test_list(self):
    nx = Nixie()
    nx.create()
    nx.create()
    keys = nx.list()
    self.assertIsInstance(keys, KeysView)
    [self.assertRegexpMatches(key, self.regexp) for key in keys]

  def test_exists(self):
    nx = Nixie()
    key1 = nx.create()
    key2 = nx.create()
    self.assertTrue(nx.exists(key1))
    self.assertTrue(nx.exists(key2))
    self.assertFalse(nx.exists('missing'))

  def test_put(self):
    nx = Nixie()
    key1 = nx.create()
    key2 = nx.create()
    self.assertEqual(nx.put(key1, 12), 12)
    self.assertEqual(nx.put(key1, 24), 24)
    self.assertEqual(nx.read(key2), 0)
    self.assertEqual(nx.put(key2, 15), 15)
    self.assertEqual(nx.put(key2, 32), 32)
    self.assertEqual(nx.read(key1), 24)
    self.assertEqual(nx.put(key1, -12), -12)
    self.assertEqual(nx.put(key2, 0), 0)
    self.assertEqual(nx.read(key1), -12)
    self.assertEqual(nx.read(key2), 0)

  def test_incr(self):
    nx = Nixie()
    key = nx.create()
    self.assertEqual(nx.read(key), 0)
    self.assertEqual(nx.incr(key), 1)
    self.assertEqual(nx.incr(key), 2)
    self.assertEqual(nx.incr(key), 3)
    self.assertEqual(nx.read(key), 3)

  def test_decr(self):
    nx = Nixie()
    key = nx.create()
    nx.put(key, 2)
    self.assertEqual(nx.read(key), 2)
    self.assertEqual(nx.decr(key), 1)
    self.assertEqual(nx.decr(key), 0)
    self.assertEqual(nx.decr(key), -1)
    self.assertEqual(nx.read(key), -1)
