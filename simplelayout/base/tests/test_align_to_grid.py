from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import login, logout
from plone.app.testing import setRoles
from simplelayout.base.testing import SL_TYPES_INTEGRATION_TESTING
from simplelayout.base.viewlets.viewlets import SimpleLayoutAlignActionViewlet
from unittest2 import TestCase
from ftw.builder import Builder
from ftw.builder import create


class TestPermission(TestCase):
    layer = SL_TYPES_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.portal.portal_types.Document.global_allow = True
        self.portal.portal_types.Paragraph.global_allow = True
        setRoles(self.portal, TEST_USER_ID, ['Contributor', 'Manager'])
        login(self.portal, TEST_USER_NAME)
        self.page = create(Builder('sl-page').titled('Hans'))
        create(Builder('paragraph').titled('Blubb').within(self.page))
        logout()

    def test_permission_reader(self):
        setRoles(self.portal, TEST_USER_ID, ['Reader'])
        login(self.portal, TEST_USER_NAME)
        viewlet = SimpleLayoutAlignActionViewlet(self.portal, self.portal.REQUEST, 'simplelayout')
        self.assertFalse(viewlet.has_permission())
        logout()

    def test_permission_editor(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor', 'Editor'])
        login(self.portal, TEST_USER_NAME)
        viewlet = SimpleLayoutAlignActionViewlet(self.portal, self.portal.REQUEST, 'simplelayout')
        self.assertTrue(viewlet.has_permission())
