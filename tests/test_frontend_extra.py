import unittest, time
from nixie.frontend import Frontend

class FrontendTestCase(unittest.TestCase):

  regexp = b'\w{21}'

  def setUp(self):
    fe = Frontend()
    self.app = fe.app.test_client

  def test_list(self):
    [self.app.post('/') for _ in range(5)]
    req, resp = self.app.get('/')
    self.assertEqual(resp.status, 200)
    self.assertTrue(resp.headers['Content-Type'].startswith('text/plain'))
    keys = resp.body.split()
    self.assertEqual(len(keys), 5)
    for key in keys:
      self.assertRegexpMatches(key, self.regexp)

  def test_empty_list(self):
    req, resp = self.app.get('/')
    self.assertEqual(resp.status, 200)
    self.assertTrue(resp.headers['Content-Type'].startswith('text/plain'))
    self.assertFalse(resp.body)

  def test_exists(self):
    key = self.get_key()
    url = '/{key}'.format(key=key)
    req, resp = self.app.head(url)
    self.assertEqual(resp.status, 204)
    self.assertFalse(resp.body)
    req, resp = self.app.head('/missing')
    self.assertEqual(resp.status, 404)
    self.assertTrue(resp.headers['Content-Type'].startswith('text/plain'))
    self.assertFalse(resp.body)

  # def test_put(self):
  #   key = self.get_key()
  #   url = '/{key}/12'.format(key=key)
  #   req, resp = self.app.put(url)
  #   self.assertEqual(resp.status, 200)
  #   self.assertTrue(resp.headers['Content-Type'].startswith('text/plain'))
  #   self.assertEqual(resp.body, b'12')
  #   url = '/{key}/24'.format(key=key)
  #   req, resp = self.app.put(url)
  #   self.assertEqual(resp.status, 200)
  #   self.assertTrue(resp.headers['Content-Type'].startswith('text/plain'))
  #   self.assertEqual(resp.body, b'24')
  #   url = '/{key}/-7'.format(key=key)
  #   req, resp = self.app.put(url)
  #   self.assertEqual(resp.status, 200)
  #   self.assertTrue(resp.headers['Content-Type'].startswith('text/plain'))
  #   self.assertEqual(resp.body, b'-7')
  #   url = '/{key}/0'.format(key=key)
  #   req, resp = self.app.put(url)
  #   self.assertEqual(resp.status, 200)
  #   self.assertTrue(resp.headers['Content-Type'].startswith('text/plain'))
  #   self.assertEqual(resp.body, b'0')

  def test_increase(self):
    key = self.get_key()
    url = '/{key}/incr'.format(key=key)
    req, resp = self.app.put(url)
    self.assertEqual(resp.status, 200)
    self.assertTrue(resp.headers['Content-Type'].startswith('text/plain'))
    self.assertEqual(resp.body, b'1')
    req, resp = self.app.put(url)
    self.assertEqual(resp.status, 200)
    self.assertTrue(resp.headers['Content-Type'].startswith('text/plain'))
    self.assertEqual(resp.body, b'2')

  def test_decrease(self):
    key = self.get_key()
    url = '/{key}/decr'.format(key=key)
    req, resp = self.app.put(url)
    self.assertEqual(resp.status, 200)
    self.assertTrue(resp.headers['Content-Type'].startswith('text/plain'))
    self.assertEqual(resp.body, b'-1')
    req, resp = self.app.put(url)
    self.assertEqual(resp.status, 200)
    self.assertTrue(resp.headers['Content-Type'].startswith('text/plain'))
    self.assertEqual(resp.body, b'-2')

  def get_key(self):
    self.app.post('/')
    req, resp = self.app.get('/')
    return resp.body.decode("utf-8")
