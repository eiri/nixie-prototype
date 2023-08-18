import unittest
from nixie.frontend import Frontend
from fastapi.testclient import TestClient

class FrontendTestCase(unittest.TestCase):

  regexp = br'\w{21}'

  def setUp(self):
    fe = Frontend()
    self.client = TestClient(fe.app)

  def test_empty_list(self):
    resp = self.client.get('/')
    self.assertEqual(resp.status_code, 200)
    self.assertTrue(resp.headers['Content-Type'].startswith('text/plain'))
    self.assertNotIn('Nixie-Step', resp.headers)
    self.assertNotIn('Nixie-Name', resp.headers)
    self.assertNotIn('Nixie-Description', resp.headers)
    self.assertFalse(resp.text)

  def test_create(self):
    for _ in range(5):
        resp = self.client.post('/')
        self.assertEqual(resp.status_code, 201)
        self.assertTrue(resp.headers['Content-Type'].startswith('text/plain'))
        self.assertEqual(resp.headers['Nixie-Step'], '1')
        self.assertNotIn('Nixie-Name', resp.headers)
        self.assertNotIn('Nixie-Description', resp.headers)
        self.assertRegex(resp.text.encode(), self.regexp)
    resp = self.client.get('/')
    self.assertEqual(resp.status_code, 200)
    self.assertTrue(resp.headers['Content-Type'].startswith('text/plain'))
    self.assertNotIn('Nixie-Step', resp.headers)
    self.assertNotIn('Nixie-Name', resp.headers)
    self.assertNotIn('Nixie-Description', resp.headers)
    keys = resp.text.split()
    self.assertEqual(len(keys), 5)
    for key in keys:
      self.assertRegex(key.encode(), self.regexp)

  def test_create_custom(self):
    # create
    headers = {
      'content-type': 'text/plain',
      'nixie-step': '3',
      'nixie-name': 'custom counter',
      'nixie-description': 'this is a custom counter'
    }
    resp = self.client.post('/', content=b'3', headers=headers)
    self.assertEqual(resp.status_code, 201)
    self.assertTrue(resp.headers['Content-Type'].startswith('text/plain'))
    self.assertEqual(resp.headers['Nixie-Step'], '3')
    self.assertEqual(resp.headers['Nixie-Name'], 'custom counter')
    self.assertEqual(resp.headers['Nixie-Description'], 'this is a custom counter')
    self.assertRegex(resp.text.encode(), self.regexp)
    # read back
    url = '/{key}'.format(key=resp.text)
    resp = self.client.get(url)
    self.assertEqual(resp.status_code, 200)
    self.assertTrue(resp.headers['Content-Type'].startswith('text/plain'))
    self.assertEqual(resp.headers['Nixie-Step'], '3')
    self.assertEqual(resp.headers['Nixie-Name'], 'custom counter')
    self.assertEqual(resp.headers['Nixie-Description'], 'this is a custom counter')
    self.assertEqual(resp.text.encode(), b'3')
    # update counter
    resp = self.client.post(url)
    self.assertEqual(resp.status_code, 200)
    self.assertTrue(resp.headers['Content-Type'].startswith('text/plain'))
    self.assertEqual(resp.headers['Nixie-Step'], '3')
    self.assertEqual(resp.headers['Nixie-Name'], 'custom counter')
    self.assertEqual(resp.headers['Nixie-Description'], 'this is a custom counter')
    self.assertEqual(resp.text.encode(), b'6')

  def test_create_custom_invalid(self):
    resp = self.client.post('/', content=b'3', headers={'nixie-step': 'a'})
    self.assertEqual(resp.status_code, 422)
    self.assertIn('Input should be a valid integer', resp.json()['detail'][0]['msg'])

  def test_read(self):
    key = self.get_key()
    url = '/{key}'.format(key=key)
    resp = self.client.get(url)
    self.assertEqual(resp.status_code, 200)
    self.assertTrue(resp.headers['Content-Type'].startswith('text/plain'))
    self.assertEqual(resp.headers['Nixie-Step'], '1')
    self.assertNotIn('Nixie-Name', resp.headers)
    self.assertNotIn('Nixie-Description', resp.headers)
    self.assertEqual(resp.text, '0')

  def test_read_missing(self):
    resp = self.client.get('/nokey')
    self.assertEqual(resp.status_code, 404)
    self.assertTrue(resp.headers['Content-Type'].startswith('application/json'))
    self.assertNotIn('Nixie-Step', resp.headers)
    self.assertNotIn('Nixie-Name', resp.headers)
    self.assertNotIn('Nixie-Description', resp.headers)
    self.assertIn('Unknown key', resp.json()['detail'])

  def test_exists(self):
    key = self.get_key()
    url = '/{key}'.format(key=key)
    resp = self.client.head(url)
    self.assertEqual(resp.status_code, 204)
    self.assertEqual(resp.headers['Nixie-Step'], '1')
    self.assertNotIn('Nixie-Name', resp.headers)
    self.assertNotIn('Nixie-Description', resp.headers)
    self.assertFalse(resp.text)

  def test_not_exists(self):
    resp = self.client.head('/nokey')
    self.assertEqual(resp.status_code, 404)
    self.assertTrue(resp.headers['Content-Type'].startswith('application/json'))
    self.assertNotIn('Nixie-Step', resp.headers)
    self.assertNotIn('Nixie-Name', resp.headers)
    self.assertNotIn('Nixie-Description', resp.headers)
    self.assertFalse(resp.text)
    # self.assertIn('Unknown key', resp.text)

  def test_update(self):
    key = self.get_key()
    url = '/{key}'.format(key=key)
    resp = self.client.post(url)
    self.assertEqual(resp.status_code, 200)
    self.assertTrue(resp.headers['Content-Type'].startswith('text/plain'))
    self.assertEqual(resp.headers['Nixie-Step'], '1')
    self.assertNotIn('Nixie-Name', resp.headers)
    self.assertNotIn('Nixie-Description', resp.headers)
    self.assertEqual(resp.text, '1')
    resp = self.client.post(url)
    self.assertEqual(resp.status_code, 200)
    self.assertTrue(resp.headers['Content-Type'].startswith('text/plain'))
    self.assertEqual(resp.headers['Nixie-Step'], '1')
    self.assertNotIn('Nixie-Name', resp.headers)
    self.assertNotIn('Nixie-Description', resp.headers)
    self.assertEqual(resp.text, '2')

  def test_update_missing(self):
    resp = self.client.post('/nokey')
    self.assertEqual(resp.status_code, 404)
    self.assertTrue(resp.headers['Content-Type'].startswith('application/json'))
    self.assertNotIn('Nixie-Step', resp.headers)
    self.assertNotIn('Nixie-Name', resp.headers)
    self.assertNotIn('Nixie-Description', resp.headers)
    self.assertIn('Unknown key', resp.json()['detail'])

  def test_patch(self):
    key = self.get_key()
    url = '/{key}'.format(key=key)
    headers = {
      'nixie-step': '3',
      'nixie-name': 'custom counter',
      'nixie-description': 'this is a custom counter'
    }
    resp = self.client.patch(url, headers=headers)
    self.assertEqual(resp.status_code, 204)
    self.assertEqual(resp.headers['Nixie-Step'], '3')
    self.assertEqual(resp.headers['Nixie-Name'], 'custom counter')
    self.assertEqual(resp.headers['Nixie-Description'], 'this is a custom counter')
    self.assertFalse(resp.text)
    # read back
    resp = self.client.get(url)
    self.assertEqual(resp.status_code, 200)
    self.assertTrue(resp.headers['Content-Type'].startswith('text/plain'))
    self.assertEqual(resp.headers['Nixie-Step'], '3')
    self.assertEqual(resp.headers['Nixie-Name'], 'custom counter')
    self.assertEqual(resp.headers['Nixie-Description'], 'this is a custom counter')
    self.assertEqual(resp.text, '0')

  def test_patch_missing(self):
    resp = self.client.patch('/nokey', headers={'nixie-step': '3'})
    self.assertEqual(resp.status_code, 404)
    self.assertTrue(resp.headers['Content-Type'].startswith('application/json'))
    self.assertNotIn('Nixie-Step', resp.headers)
    self.assertNotIn('Nixie-Name', resp.headers)
    self.assertNotIn('Nixie-Description', resp.headers)
    self.assertIn('Unknown key', resp.json()['detail'])

  def test_delete(self):
    key = self.get_key()
    url = '/{key}'.format(key=key)
    resp = self.client.delete(url)
    self.assertEqual(resp.status_code, 204)
    self.assertNotIn('Nixie-Step', resp.headers)
    self.assertNotIn('Nixie-Name', resp.headers)
    self.assertNotIn('Nixie-Description', resp.headers)
    self.assertFalse(resp.text)

  def test_delete_missing(self):
    resp = self.client.delete('/nokey')
    self.assertEqual(resp.status_code, 404)
    self.assertTrue(resp.headers['Content-Type'].startswith('application/json'))
    self.assertNotIn('Nixie-Step', resp.headers)
    self.assertNotIn('Nixie-Name', resp.headers)
    self.assertNotIn('Nixie-Description', resp.headers)
    self.assertIn('Unknown key', resp.json()['detail'])

  def get_key(self):
    self.client.post('/')
    resp = self.client.get('/')
    return resp.text
