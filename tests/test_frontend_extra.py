import unittest, time
from nixie.frontend import Frontend

class FrontendTestCase(unittest.TestCase):

  regexp = b'[a-f0-9]{32}'

  def setUp(self):
    fe = Frontend()
    fe.apptesting = True
    self.app = fe.app.test_client()

  def test_list(self):
    [self.app.post('/') for _ in range(5)]
    resp = self.app.get('/')
    self.assertEqual(resp.status_code, 200)
    self.assertTrue(resp.headers['Content-Type'].startswith('text/plain'))
    keys = resp.data.split()
    self.assertEqual(len(keys), 5)
    for key in keys:
      self.assertRegexpMatches(key, self.regexp)

  def test_empty_list(self):
    resp = self.app.get('/')
    self.assertEqual(resp.status_code, 200)
    self.assertTrue(resp.headers['Content-Type'].startswith('text/plain'))
    self.assertFalse(resp.data)

  def test_exists(self):
    key = self.get_key()
    url = '/{key}'.format(key=key)
    resp = self.app.head(url)
    self.assertEqual(resp.status_code, 200)
    self.assertTrue(resp.headers['Content-Type'].startswith('text/plain'))
    self.assertFalse(resp.data)
    resp = self.app.head('/missing')
    self.assertEqual(resp.status_code, 404)
    self.assertTrue(resp.headers['Content-Type'].startswith('text/plain'))
    self.assertFalse(resp.data)

  def test_put(self):
    key = self.get_key()
    url = '/{key}/12'.format(key=key)
    resp = self.app.put(url)
    self.assertEqual(resp.status_code, 200)
    self.assertTrue(resp.headers['Content-Type'].startswith('text/plain'))
    self.assertEqual(resp.data, b'12')
    url = '/{key}/24'.format(key=key)
    resp = self.app.put(url)
    self.assertEqual(resp.status_code, 200)
    self.assertTrue(resp.headers['Content-Type'].startswith('text/plain'))
    self.assertEqual(resp.data, b'24')
    url = '/{key}/-7'.format(key=key)
    resp = self.app.put(url)
    self.assertEqual(resp.status_code, 200)
    self.assertTrue(resp.headers['Content-Type'].startswith('text/plain'))
    self.assertEqual(resp.data, b'-7')
    url = '/{key}/0'.format(key=key)
    resp = self.app.put(url)
    self.assertEqual(resp.status_code, 200)
    self.assertTrue(resp.headers['Content-Type'].startswith('text/plain'))
    self.assertEqual(resp.data, b'0')

  def test_increase(self):
    key = self.get_key()
    url = '/{key}/incr'.format(key=key)
    resp = self.app.put(url)
    self.assertEqual(resp.status_code, 200)
    self.assertTrue(resp.headers['Content-Type'].startswith('text/plain'))
    self.assertEqual(resp.data, b'1')
    resp = self.app.put(url)
    self.assertEqual(resp.status_code, 200)
    self.assertTrue(resp.headers['Content-Type'].startswith('text/plain'))
    self.assertEqual(resp.data, b'2')

  def test_decrease(self):
    key = self.get_key()
    url = '/{key}/decr'.format(key=key)
    resp = self.app.put(url)
    self.assertEqual(resp.status_code, 200)
    self.assertTrue(resp.headers['Content-Type'].startswith('text/plain'))
    self.assertEqual(resp.data, b'-1')
    resp = self.app.put(url)
    self.assertEqual(resp.status_code, 200)
    self.assertTrue(resp.headers['Content-Type'].startswith('text/plain'))
    self.assertEqual(resp.data, b'-2')

  def get_key(self):
    self.app.post('/')
    resp = self.app.get('/')
    return resp.data.decode("utf-8")
