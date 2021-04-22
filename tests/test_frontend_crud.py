import unittest, time
from nixie.frontend import Frontend

class FrontendTestCase(unittest.TestCase):

  regexp = br'\w{21}'

  def setUp(self):
    fe = Frontend()
    self.app = fe.app.test_client

  def test_empty_list(self):
    req, resp = self.app.get('/')
    self.assertEqual(resp.status, 200)
    self.assertTrue(resp.headers['Content-Type'].startswith('text/plain'))
    self.assertFalse(resp.body)

  def test_create(self):
    for _ in range(5):
        req, resp = self.app.post('/')
        self.assertEqual(resp.status, 201)
        self.assertTrue(resp.headers['Content-Type'].startswith('text/plain'))
        self.assertRegex(resp.body, self.regexp)
    req, resp = self.app.get('/')
    self.assertEqual(resp.status, 200)
    self.assertTrue(resp.headers['Content-Type'].startswith('text/plain'))
    keys = resp.body.split()
    self.assertEqual(len(keys), 5)
    for key in keys:
      self.assertRegex(key, self.regexp)

  def test_read(self):
    key = self.get_key()
    url = '/{key}'.format(key=key)
    req, resp = self.app.get(url)
    self.assertEqual(resp.status, 200)
    self.assertTrue(resp.headers['Content-Type'].startswith('text/plain'))
    self.assertEqual(resp.body, b'0')

  def test_read_missing(self):
    req, resp = self.app.get('/nokey')
    self.assertEqual(resp.status, 404)
    self.assertTrue(resp.headers['Content-Type'].startswith('text/plain'))
    self.assertIn(b'Not Found', resp.body)

  def test_exists(self):
    key = self.get_key()
    url = '/{key}'.format(key=key)
    req, resp = self.app.head(url)
    self.assertEqual(resp.status, 204)
    self.assertFalse(resp.body)

  def test_not_exists(self):
    req, resp = self.app.head('/nokey')
    self.assertEqual(resp.status, 404)
    self.assertTrue(resp.headers['Content-Type'].startswith('text/plain'))
    self.assertFalse(resp.body)

  def test_update(self):
    key = self.get_key()
    url = '/{key}'.format(key=key)
    req, resp = self.app.post(url)
    self.assertEqual(resp.status, 200)
    self.assertTrue(resp.headers['Content-Type'].startswith('text/plain'))
    self.assertEqual(resp.body, b'1')
    req, resp = self.app.post(url)
    self.assertEqual(resp.status, 200)
    self.assertTrue(resp.headers['Content-Type'].startswith('text/plain'))
    self.assertEqual(resp.body, b'2')

  def test_update_missing(self):
    req, resp = self.app.post('/nokey')
    self.assertEqual(resp.status, 404)
    self.assertTrue(resp.headers['Content-Type'].startswith('text/plain'))
    self.assertIn(b'Not Found', resp.body)

  def test_delete(self):
    key = self.get_key()
    url = '/{key}'.format(key=key)
    req, resp = self.app.delete(url)
    self.assertEqual(resp.status, 204)
    self.assertFalse(resp.body)

  def test_delete_missing(self):
    req, resp = self.app.delete('/nokey')
    self.assertEqual(resp.status, 404)
    self.assertTrue(resp.headers['Content-Type'].startswith('text/plain'))
    self.assertIn(b'Not Found', resp.body)

  def get_key(self):
    self.app.post('/')
    req, resp = self.app.get('/')
    return resp.body.decode("utf-8")
