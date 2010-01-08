import unittest
import doctest

from zope.testing import doctestunit
from zope.component import testing, eventtesting

from Testing import ZopeTestCase as ztc

from plonegov.website.tests import base

def test_suite():
    return unittest.TestSuite([

        # Demonstrate the main content types
        ztc.ZopeDocFileSuite(
            'browser.txt', package='simplelayout.base',
            test_class=base.SimplelayoutFunctionalTestCase,
            optionflags=doctest.REPORT_ONLY_FIRST_FAILURE | doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS),


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')

