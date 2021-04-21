import unittest, time
from nixie.frontend import Frontend

class FrontendTestCase(unittest.TestCase):

  regexp = b'\w{21}'

  def setUp(self):
    fe = Frontend()
    self.app = fe.app.test_client

  def test_create(self):
    req, resp = self.app.post('/')
    self.assertEqual(resp.status, 201)
    self.assertTrue(resp.headers['Content-Type'].startswith('text/plain'))
    self.assertRegexpMatches(resp.body, self.regexp)

  def test_read(self):
    key = self.get_key()
    url = '/{key}'.format(key=key)
    req, resp = self.app.get(url)
    self.assertEqual(resp.status, 200)
    self.assertTrue(resp.headers['Content-Type'].startswith('text/plain'))
    self.assertEqual(resp.body, b'0')

  def test_update_incr(self):
    key = self.get_key()
    url = '/{key}/incr/12'.format(key=key)
    req, resp = self.app.put(url)
    self.assertEqual(resp.status, 200)
    self.assertTrue(resp.headers['Content-Type'].startswith('text/plain'))
    self.assertEqual(resp.body, b'12')
    req, resp = self.app.put(url)
    self.assertEqual(resp.status, 200)
    self.assertTrue(resp.headers['Content-Type'].startswith('text/plain'))
    self.assertEqual(resp.body, b'24')

  def test_update_decr(self):
    key = self.get_key()
    req, resp = self.app.put('/{key}/incr/17'.format(key=key))
    url = '/{key}/decr/6'.format(key=key)
    req, resp = self.app.put(url)
    self.assertEqual(resp.status, 200)
    self.assertTrue(resp.headers['Content-Type'].startswith('text/plain'))
    self.assertEqual(resp.body, b'11')
    req, resp = self.app.put(url)
    self.assertEqual(resp.status, 200)
    self.assertTrue(resp.headers['Content-Type'].startswith('text/plain'))
    self.assertEqual(resp.body, b'5')

  def test_delete(self):
    key = self.get_key()
    url = '/{key}'.format(key=key)
    req, resp = self.app.delete(url)
    self.assertEqual(resp.status, 204)
    self.assertFalse(resp.body)

  def get_key(self):
    self.app.post('/')
    req, resp = self.app.get('/')
    return resp.body.decode("utf-8")
