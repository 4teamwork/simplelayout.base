from ftw.builder import Builder
from ftw.builder import create
from ftw.testbrowser import browsing
from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles
from simplelayout.base.interfaces import ISimpleLayoutBlock
from simplelayout.base.testing import SL_BASE_FUNCTIONAL_TESTING
from unittest2 import TestCase


class TestParagraphView(TestCase):
    layer = SL_BASE_FUNCTIONAL_TESTING

    def setUp(self):
        setRoles(self.layer['portal'], TEST_USER_ID, ['Contributor'])

    @browsing
    def test_paragraph_view_redirects_to_container(self, browser):
        folder = create(Builder('folder')
                        .titled('The Folder'))

        block = create(Builder('file')
                       .titled('The Block')
                       .providing(ISimpleLayoutBlock)
                       .within(folder))

        browser.open(block, view='paragraph_view')
        self.assertEquals(folder, browser.context,
                          'The paragraph_view should redirect to the container.')
        self.assertEquals(folder.absolute_url() + '/#the-block', browser.url)
