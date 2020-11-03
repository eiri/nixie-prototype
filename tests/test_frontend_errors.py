import unittest, time
from nixie.frontend import Frontend

class FrontendTestCase(unittest.TestCase):

  regexp = b'[a-f0-9]{32}'

  def setUp(self):
    fe = Frontend()
    fe.apptesting = True
    self.app = fe.app.test_client()

  def test_read_missing(self):
    resp = self.app.get('/nokey')
    self.assertEqual(resp.status_code, 404)
    self.assertTrue(resp.headers['Content-Type'].startswith('text/plain'))
    self.assertFalse(resp.data)

  def test_increase_missing(self):
    resp = self.app.put('/nokey/incr')
    self.assertEqual(resp.status_code, 404)
    self.assertTrue(resp.headers['Content-Type'].startswith('text/plain'))
    self.assertEqual(resp.data, b'Unknown key nokey')

  def test_increase_invalid(self):
    key = self.get_key()
    url = '/{key}/incr/noint'.format(key=key)
    resp = self.app.put(url)
    self.assertEqual(resp.status_code, 400)
    self.assertTrue(resp.headers['Content-Type'].startswith('text/plain'))
    self.assertEqual(resp.data, b'Invalid value noint')

  def test_decrease_missing(self):
    resp = self.app.put('/nokey/decr')
    self.assertEqual(resp.status_code, 404)
    self.assertTrue(resp.headers['Content-Type'].startswith('text/plain'))
    self.assertEqual(resp.data, b'Unknown key nokey')

  def test_decrease_invalid(self):
    key = self.get_key()
    url = '/{key}/decr/noint'.format(key=key)
    resp = self.app.put(url)
    self.assertEqual(resp.status_code, 400)
    self.assertTrue(resp.headers['Content-Type'].startswith('text/plain'))
    self.assertEqual(resp.data, b'Invalid value -noint')

  def test_put_missing(self):
    resp = self.app.put('/nokey/12')
    self.assertEqual(resp.status_code, 404)
    self.assertTrue(resp.headers['Content-Type'].startswith('text/plain'))
    self.assertEqual(resp.data, b'Unknown key nokey')

  def test_put_invalid(self):
    key = self.get_key()
    url = '/{key}/noint'.format(key=key)
    resp = self.app.put(url)
    self.assertEqual(resp.status_code, 400)
    self.assertTrue(resp.headers['Content-Type'].startswith('text/plain'))
    self.assertEqual(resp.data, b'Invalid value noint')

  def test_delete_missing(self):
    resp = self.app.delete('/nokey')
    self.assertEqual(resp.status_code, 404)
    self.assertTrue(resp.headers['Content-Type'].startswith('text/plain'))
    self.assertEqual(resp.data, b'Unknown key nokey')

  def get_key(self):
    self.app.post('/')
    resp = self.app.get('/')
    return resp.data.decode("utf-8")
