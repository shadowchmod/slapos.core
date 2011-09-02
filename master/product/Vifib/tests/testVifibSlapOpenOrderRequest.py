import unittest
from testVifibSlapWebService import TestVifibSlapWebServiceMixin

class TestVifibSlapOpenOrderRequest(TestVifibSlapWebServiceMixin):

def test_suite():
  suite = unittest.TestSuite()
  suite.addTest(unittest.makeSuite(TestVifibSlapOpenOrderRequest))
  return suite
