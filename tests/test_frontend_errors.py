import unittest, time
from nixie.frontend import Frontend

class FrontendTestCase(unittest.TestCase):

  regexp = '[a-f0-9]{32}'

  def setUp(self):
    fe = Frontend()
    fe.apptesting = True
    self.app = fe.app.test_client()

  def test_read_missing(self):
    resp = self.app.get('/missing')
    self.assertEqual(resp.status_code, 404)
    self.assertTrue(resp.headers['Content-Type'].startswith('text/plain'))
    self.assertFalse(resp.data)

  def test_increase_missing(self):
    resp = self.app.put('/missing/incr')
    self.assertEqual(resp.status_code, 404)
    self.assertTrue(resp.headers['Content-Type'].startswith('text/plain'))
    self.assertEqual(resp.data, 'Unknown key missing')

  def test_increase_invalid(self):
    key = self.get_key()
    url = '/{key}/incr/noint'.format(key=key)
    resp = self.app.put(url)
    self.assertEqual(resp.status_code, 400)
    self.assertTrue(resp.headers['Content-Type'].startswith('text/plain'))
    self.assertEqual(resp.data, 'Invalid value noint')

  def test_decrease_missing(self):
    resp = self.app.put('/missing/decr')
    self.assertEqual(resp.status_code, 404)
    self.assertTrue(resp.headers['Content-Type'].startswith('text/plain'))
    self.assertEqual(resp.data, 'Unknown key missing')

  def test_decrease_invalid(self):
    key = self.get_key()
    url = '/{key}/decr/noint'.format(key=key)
    resp = self.app.put(url)
    self.assertEqual(resp.status_code, 400)
    self.assertTrue(resp.headers['Content-Type'].startswith('text/plain'))
    self.assertEqual(resp.data, 'Invalid value -noint')

  def test_put_missing(self):
    resp = self.app.put('/missing/12')
    self.assertEqual(resp.status_code, 404)
    self.assertTrue(resp.headers['Content-Type'].startswith('text/plain'))
    self.assertEqual(resp.data, 'Unknown key missing')

  def test_put_invalid(self):
    key = self.get_key()
    url = '/{key}/noint'.format(key=key)
    resp = self.app.put(url)
    self.assertEqual(resp.status_code, 400)
    self.assertTrue(resp.headers['Content-Type'].startswith('text/plain'))
    self.assertEqual(resp.data, 'Invalid value noint')

  def test_delete_missing(self):
    resp = self.app.delete('/missing')
    self.assertEqual(resp.status_code, 404)
    self.assertTrue(resp.headers['Content-Type'].startswith('text/plain'))
    self.assertEqual(resp.data, 'Unknown key missing')

  def get_key(self):
    self.app.post('/')
    resp = self.app.get('/')
    return resp.data
