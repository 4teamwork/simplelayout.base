import unittest2 as unittest
import doctest
from plone.testing import layered
from simplelayout.base.testing import SL_BASE_INTEGRATION_TESTING


DOCTEST_FILES = [
    'delete_blocks.txt',
    '../browser.txt',
    ]


def test_suite():
    suite = unittest.TestSuite()
    for doctest_file in DOCTEST_FILES:
        suite.addTests([
            layered(doctest.DocFileSuite(doctest_file),
                    layer=SL_BASE_INTEGRATION_TESTING),
        ])
    return suite
