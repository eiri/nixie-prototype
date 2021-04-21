import unittest, time
from nixie.frontend import Frontend

class FrontendTestCase(unittest.TestCase):

  regexp = b'\w{21}'

  def setUp(self):
    fe = Frontend()
    self.app = fe.app.test_client

  def test_read_missing(self):
    req, resp = self.app.get('/nokey')
    self.assertEqual(resp.status, 404)
    self.assertTrue(resp.headers['Content-Type'].startswith('text/plain'))
    self.assertIn(b'Not Found', resp.body)

  def test_increase_missing(self):
    req, resp = self.app.put('/nokey/incr')
    self.assertEqual(resp.status, 404)
    self.assertTrue(resp.headers['Content-Type'].startswith('text/plain'))
    self.assertIn(b'Unknown key nokey', resp.body)

  def test_increase_invalid(self):
    key = self.get_key()
    url = '/{key}/incr/noint'.format(key=key)
    req, resp = self.app.put(url)
    self.assertEqual(resp.status, 404)
    self.assertTrue(resp.headers['Content-Type'].startswith('text/plain'))
    self.assertIn(b'Not Found', resp.body)

  def test_decrease_missing(self):
    req, resp = self.app.put('/nokey/decr')
    self.assertEqual(resp.status, 404)
    self.assertTrue(resp.headers['Content-Type'].startswith('text/plain'))
    self.assertIn(b'Unknown key nokey', resp.body)

  def test_decrease_invalid(self):
    key = self.get_key()
    url = '/{key}/decr/noint'.format(key=key)
    req, resp = self.app.put(url)
    self.assertEqual(resp.status, 404)
    self.assertTrue(resp.headers['Content-Type'].startswith('text/plain'))
    self.assertIn(b'Not Found', resp.body)

  # def test_put_missing(self):
  #   req, resp = self.app.put('/nokey/12')
  #   self.assertEqual(resp.status, 404)
  #   self.assertTrue(resp.headers['Content-Type'].startswith('text/plain'))
  #   self.assertIn(b'Not Found', resp.body)

  # def test_put_invalid(self):
  #   key = self.get_key()
  #   url = '/{key}/noint'.format(key=key)
  #   req, resp = self.app.put(url)
  #   self.assertEqual(resp.status, 400)
  #   self.assertTrue(resp.headers['Content-Type'].startswith('text/plain'))
  #   self.assertEqual(resp.body, b'Invalid value noint')

  def test_delete_missing(self):
    req, resp = self.app.delete('/nokey')
    self.assertEqual(resp.status, 404)
    self.assertTrue(resp.headers['Content-Type'].startswith('text/plain'))
    self.assertIn(b'Not Found', resp.body)

  def get_key(self):
    self.app.post('/')
    req, resp = self.app.get('/')
    return resp.body.decode("utf-8")
