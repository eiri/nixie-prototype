import unittest
from nixie import nixie

class NixieTestCase(unittest.TestCase):
  def test_do_mock(self):
    self.assertTrue(nixie.do_mock())
