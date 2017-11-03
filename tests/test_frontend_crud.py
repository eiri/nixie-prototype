import unittest, time
from nixie.frontend import Frontend

class FrontendTestCase(unittest.TestCase):

  regexp = '[a-f0-9]{32}'

  def setUp(self):
    fe = Frontend()
    fe.apptesting = True
    self.app = fe.app.test_client()

  def test_create(self):
    resp = self.app.post('/')
    self.assertEqual(resp.status_code, 201)
    self.assertTrue(resp.headers['Content-Type'].startswith('text/plain'))
    self.assertRegexpMatches(resp.data, self.regexp)

  def test_read(self):
    key = self.get_key()
    url = '/{key}'.format(key=key)
    resp = self.app.get(url)
    self.assertEqual(resp.status_code, 200)
    self.assertTrue(resp.headers['Content-Type'].startswith('text/plain'))
    self.assertEqual(resp.data, '0')

  def test_update_incr(self):
    key = self.get_key()
    url = '/{key}/incr/12'.format(key=key)
    resp = self.app.put(url)
    self.assertEqual(resp.status_code, 200)
    self.assertTrue(resp.headers['Content-Type'].startswith('text/plain'))
    self.assertEqual(resp.data, '12')
    resp = self.app.put(url)
    self.assertEqual(resp.status_code, 200)
    self.assertTrue(resp.headers['Content-Type'].startswith('text/plain'))
    self.assertEqual(resp.data, '24')

  def test_update_decr(self):
    key = self.get_key()
    resp = self.app.put('/{key}/incr/17'.format(key=key))
    url = '/{key}/decr/6'.format(key=key)
    resp = self.app.put(url)
    self.assertEqual(resp.status_code, 200)
    self.assertTrue(resp.headers['Content-Type'].startswith('text/plain'))
    self.assertEqual(resp.data, '11')
    resp = self.app.put(url)
    self.assertEqual(resp.status_code, 200)
    self.assertTrue(resp.headers['Content-Type'].startswith('text/plain'))
    self.assertEqual(resp.data, '5')

  def test_delete(self):
    key = self.get_key()
    url = '/{key}'.format(key=key)
    resp = self.app.delete(url)
    self.assertEqual(resp.status_code, 204)
    self.assertTrue(resp.headers['Content-Type'].startswith('text/plain'))
    self.assertFalse(resp.data)

  def get_key(self):
    self.app.post('/')
    resp = self.app.get('/')
    return resp.data
