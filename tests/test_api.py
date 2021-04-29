import unittest
from nixie.api import Nixie, KeyError

class APITestCase(unittest.TestCase):

  regexp = r'\w{21}'

  def setUp(self):
    self.nx = Nixie()
    self.key1 = self.nx.create()
    self.key2 = self.nx.create()

  def test_create(self):
    self.assertRegex(self.key1, self.regexp)
    self.assertRegex(self.key2, self.regexp)
    self.assertNotEqual(self.key1, self.key2)

  def test_read(self):
    self.assertEqual(self.nx.read(self.key1), 0)
    self.assertEqual(self.nx.read(self.key2), 0)

  def test_read_missing(self):
    with self.assertRaises(KeyError):
      self.nx.read('missing')

  def test_update(self):
    self.assertEqual(self.nx.read(self.key1), 0)
    self.assertEqual(self.nx.update(self.key1, 4), 4)
    self.assertEqual(self.nx.update(self.key1, 8), 8)
    self.assertEqual(self.nx.read(self.key2), 0)
    self.assertEqual(self.nx.update(self.key2, 5), 5)
    self.assertEqual(self.nx.update(self.key2, -10), -10)

  def test_update_missing(self):
    with self.assertRaises(KeyError):
      self.nx.update('missing', 5)

  def test_update_invalid(self):
    with self.assertRaises(ValueError):
      self.nx.update(self.key1, 'boom')

  def test_delete(self):
    self.assertTrue(self.nx.delete(self.key1))
    self.assertFalse(self.nx.exists(self.key1))
    self.assertTrue(self.nx.exists(self.key2))
    self.assertTrue(self.nx.delete(self.key2))
    self.assertFalse(self.nx.exists(self.key2))

  def test_delete_missing(self):
    with self.assertRaises(KeyError):
      self.nx.delete('missing')

  def test_crud_none_default(self):
    key3 = self.nx.create(3, 3, "key3", "description of key3")
    self.assertRegex(key3, self.regexp)
    self.assertEqual(self.nx.read(key3), 3)
    self.assertEqual(self.nx.next(key3), 6)
    meta3 = self.nx.read_meta(key3)
    self.assertEqual(meta3['step'], 3)
    self.assertEqual(meta3['name'], 'key3')
    self.assertEqual(meta3['description'], 'description of key3')

  def test_list(self):
    for key in self.nx.list():
      self.assertRegex(key, self.regexp)

  def test_exists(self):
    self.assertTrue(self.nx.exists(self.key1))
    self.assertTrue(self.nx.exists(self.key2))
    self.assertFalse(self.nx.exists('missing'))

  def test_next(self):
    self.assertEqual(self.nx.next(self.key1), 1)
    self.assertEqual(self.nx.next(self.key1), 2)
    self.assertEqual(self.nx.next(self.key1), 3)
    self.assertEqual(self.nx.read(self.key2), 0)
    self.assertEqual(self.nx.next(self.key2), 1)
    self.assertEqual(self.nx.read(self.key2), 1)

  def test_read_meta_default(self):
    meta1 = self.nx.read_meta(self.key1)
    self.assertEqual(meta1['step'], 1)
    self.assertIsNone(meta1['name'])
    self.assertIsNone(meta1['description'])

  def test_read_meta_missing(self):
    with self.assertRaises(KeyError):
      self.nx.read_meta('missing')

  def test_update_meta(self):
    self.nx.update_meta(self.key1, 2)
    meta1 = self.nx.read_meta(self.key1)
    self.assertEqual(meta1['step'], 2)
    self.assertIsNone(meta1['name'])
    self.assertIsNone(meta1['description'])
    self.nx.update_meta(self.key1, name='new name')
    meta1 = self.nx.read_meta(self.key1)
    self.assertEqual(meta1['step'], 2)
    self.assertEqual(meta1['name'], 'new name')
    self.assertIsNone(meta1['description'])
    self.nx.update_meta(self.key1, description='new description')
    meta1 = self.nx.read_meta(self.key1)
    self.assertEqual(meta1['step'], 2)
    self.assertEqual(meta1['name'], 'new name')
    self.assertEqual(meta1['description'], 'new description')
    meta2 = self.nx.read_meta(self.key2)
    self.assertEqual(meta2['step'], 1)
    self.assertIsNone(meta2['name'])
    self.assertIsNone(meta2['description'])
