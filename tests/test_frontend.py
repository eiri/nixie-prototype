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
    self.assertNotIn('Nixie-Step', resp.headers)
    self.assertNotIn('Nixie-Name', resp.headers)
    self.assertNotIn('Nixie-Description', resp.headers)
    self.assertFalse(resp.body)

  def test_create(self):
    for _ in range(5):
        req, resp = self.app.post('/')
        self.assertEqual(resp.status, 201)
        self.assertTrue(resp.headers['Content-Type'].startswith('text/plain'))
        self.assertEqual(resp.headers['Nixie-Step'], '1')
        self.assertNotIn('Nixie-Name', resp.headers)
        self.assertNotIn('Nixie-Description', resp.headers)
        self.assertRegex(resp.body, self.regexp)
    req, resp = self.app.get('/')
    self.assertEqual(resp.status, 200)
    self.assertTrue(resp.headers['Content-Type'].startswith('text/plain'))
    self.assertNotIn('Nixie-Step', resp.headers)
    self.assertNotIn('Nixie-Name', resp.headers)
    self.assertNotIn('Nixie-Description', resp.headers)
    keys = resp.body.split()
    self.assertEqual(len(keys), 5)
    for key in keys:
      self.assertRegex(key, self.regexp)

  def test_create_custom(self):
    # create
    headers = {
      'content-type': 'text/plain',
      'nixie-step': '3',
      'nixie-name': 'custom counter',
      'nixie-description': 'this is a custom counter'
    }
    req, resp = self.app.post('/', data='3', headers=headers)
    self.assertEqual(resp.status, 201)
    self.assertTrue(resp.headers['Content-Type'].startswith('text/plain'))
    self.assertEqual(resp.headers['Nixie-Step'], '3')
    self.assertEqual(resp.headers['Nixie-Name'], 'custom counter')
    self.assertEqual(resp.headers['Nixie-Description'], 'this is a custom counter')
    self.assertRegex(resp.body, self.regexp)
    # read back
    key = resp.body.decode("utf-8")
    url = '/{key}'.format(key=key)
    req, resp = self.app.get(url)
    self.assertEqual(resp.status, 200)
    self.assertTrue(resp.headers['Content-Type'].startswith('text/plain'))
    self.assertEqual(resp.headers['Nixie-Step'], '3')
    self.assertEqual(resp.headers['Nixie-Name'], 'custom counter')
    self.assertEqual(resp.headers['Nixie-Description'], 'this is a custom counter')
    self.assertEqual(resp.body, b'3')
    # update counter
    req, resp = self.app.post(url)
    self.assertEqual(resp.status, 200)
    self.assertTrue(resp.headers['Content-Type'].startswith('text/plain'))
    self.assertEqual(resp.headers['Nixie-Step'], '3')
    self.assertEqual(resp.headers['Nixie-Name'], 'custom counter')
    self.assertEqual(resp.headers['Nixie-Description'], 'this is a custom counter')
    self.assertEqual(resp.body, b'6')

  def test_create_custom_invalid(self):
    req, resp = self.app.post('/', data='a')
    self.assertEqual(resp.status, 500)
    self.assertIn(b'Internal Server Error', resp.body)
    req, resp = self.app.post('/', data='3', headers={'nixie-step': 'a'})
    self.assertEqual(resp.status, 500)
    self.assertIn(b'Internal Server Error', resp.body)

  def test_read(self):
    key = self.get_key()
    url = '/{key}'.format(key=key)
    req, resp = self.app.get(url)
    self.assertEqual(resp.status, 200)
    self.assertTrue(resp.headers['Content-Type'].startswith('text/plain'))
    self.assertEqual(resp.headers['Nixie-Step'], '1')
    self.assertNotIn('Nixie-Name', resp.headers)
    self.assertNotIn('Nixie-Description', resp.headers)
    self.assertEqual(resp.body, b'0')

  def test_read_missing(self):
    req, resp = self.app.get('/nokey')
    self.assertEqual(resp.status, 404)
    self.assertTrue(resp.headers['Content-Type'].startswith('text/plain'))
    self.assertNotIn('Nixie-Step', resp.headers)
    self.assertNotIn('Nixie-Name', resp.headers)
    self.assertNotIn('Nixie-Description', resp.headers)
    self.assertIn(b'Not Found', resp.body)

  def test_exists(self):
    key = self.get_key()
    url = '/{key}'.format(key=key)
    req, resp = self.app.head(url)
    self.assertEqual(resp.status, 204)
    self.assertEqual(resp.headers['Nixie-Step'], '1')
    self.assertNotIn('Nixie-Name', resp.headers)
    self.assertNotIn('Nixie-Description', resp.headers)
    self.assertFalse(resp.body)

  def test_not_exists(self):
    req, resp = self.app.head('/nokey')
    self.assertEqual(resp.status, 404)
    self.assertTrue(resp.headers['Content-Type'].startswith('text/plain'))
    self.assertNotIn('Nixie-Step', resp.headers)
    self.assertNotIn('Nixie-Name', resp.headers)
    self.assertNotIn('Nixie-Description', resp.headers)
    self.assertFalse(resp.body)

  def test_update(self):
    key = self.get_key()
    url = '/{key}'.format(key=key)
    req, resp = self.app.post(url)
    self.assertEqual(resp.status, 200)
    self.assertTrue(resp.headers['Content-Type'].startswith('text/plain'))
    self.assertEqual(resp.headers['Nixie-Step'], '1')
    self.assertNotIn('Nixie-Name', resp.headers)
    self.assertNotIn('Nixie-Description', resp.headers)
    self.assertEqual(resp.body, b'1')
    req, resp = self.app.post(url)
    self.assertEqual(resp.status, 200)
    self.assertTrue(resp.headers['Content-Type'].startswith('text/plain'))
    self.assertEqual(resp.headers['Nixie-Step'], '1')
    self.assertNotIn('Nixie-Name', resp.headers)
    self.assertNotIn('Nixie-Description', resp.headers)
    self.assertEqual(resp.body, b'2')

  def test_update_missing(self):
    req, resp = self.app.post('/nokey')
    self.assertEqual(resp.status, 404)
    self.assertTrue(resp.headers['Content-Type'].startswith('text/plain'))
    self.assertNotIn('Nixie-Step', resp.headers)
    self.assertNotIn('Nixie-Name', resp.headers)
    self.assertNotIn('Nixie-Description', resp.headers)
    self.assertIn(b'Not Found', resp.body)

  def test_patch(self):
    key = self.get_key()
    url = '/{key}'.format(key=key)
    headers = {
      'nixie-step': '3',
      'nixie-name': 'custom counter',
      'nixie-description': 'this is a custom counter'
    }
    req, resp = self.app.patch(url, headers=headers)
    self.assertEqual(resp.status, 204)
    self.assertEqual(resp.headers['Nixie-Step'], '3')
    self.assertEqual(resp.headers['Nixie-Name'], 'custom counter')
    self.assertEqual(resp.headers['Nixie-Description'], 'this is a custom counter')
    self.assertFalse(resp.body)
    # read back
    req, resp = self.app.get(url)
    self.assertEqual(resp.status, 200)
    self.assertTrue(resp.headers['Content-Type'].startswith('text/plain'))
    self.assertEqual(resp.headers['Nixie-Step'], '3')
    self.assertEqual(resp.headers['Nixie-Name'], 'custom counter')
    self.assertEqual(resp.headers['Nixie-Description'], 'this is a custom counter')
    self.assertEqual(resp.body, b'0')

  def test_patch_missing(self):
    req, resp = self.app.patch('/nokey', headers={'nixie-step': '3'})
    self.assertEqual(resp.status, 404)
    self.assertTrue(resp.headers['Content-Type'].startswith('text/plain'))
    self.assertNotIn('Nixie-Step', resp.headers)
    self.assertNotIn('Nixie-Name', resp.headers)
    self.assertNotIn('Nixie-Description', resp.headers)
    self.assertIn(b'Not Found', resp.body)

  def test_delete(self):
    key = self.get_key()
    url = '/{key}'.format(key=key)
    req, resp = self.app.delete(url)
    self.assertEqual(resp.status, 204)
    self.assertNotIn('Nixie-Step', resp.headers)
    self.assertNotIn('Nixie-Name', resp.headers)
    self.assertNotIn('Nixie-Description', resp.headers)
    self.assertFalse(resp.body)

  def test_delete_missing(self):
    req, resp = self.app.delete('/nokey')
    self.assertEqual(resp.status, 404)
    self.assertTrue(resp.headers['Content-Type'].startswith('text/plain'))
    self.assertNotIn('Nixie-Step', resp.headers)
    self.assertNotIn('Nixie-Name', resp.headers)
    self.assertNotIn('Nixie-Description', resp.headers)
    self.assertIn(b'Not Found', resp.body)

  def get_key(self):
    self.app.post('/')
    req, resp = self.app.get('/')
    return resp.body.decode("utf-8")
