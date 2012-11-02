from plone.app.testing import setRoles, login
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME, TEST_USER_PASSWORD
from plone.testing.z2 import Browser
from simplelayout.base.interfaces import ISimpleLayoutCapable
from simplelayout.base.testing import SL_BASE_INTEGRATION_TESTING
from unittest2 import TestCase
import transaction


class TestPageCreation(TestCase):

    layer = SL_BASE_INTEGRATION_TESTING

    def setUp(self):
        super(TestPageCreation, self).setUp()
        self.portal = self.layer['portal']
        self.portal_url = self.portal.portal_url()

        # Browser setup
        self.browser = Browser(self.layer['app'])
        self.browser.handleErrors = False
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        login(self.portal, TEST_USER_NAME)

    def _auth(self):
        self.browser.addHeader('Authorization', 'Basic %s:%s' % (
                TEST_USER_NAME, TEST_USER_PASSWORD, ))

    def test_fti(self):
        self.assertIn('Page', self.portal.portal_types.objectIds())

    def test_creation(self):
        _id = self.portal.invokeFactory('Page', 'page')
        self.assertIn(_id, self.portal.objectIds())

    def test_simplelayout_integration(self):
        page = self.portal.get(
            self.portal.invokeFactory('Page', 'page'))
        page.processForm()

        self.assertTrue(ISimpleLayoutCapable.providedBy(page))

    def test_simplelayout_view(self):
        _id = self.portal.invokeFactory('Page', 'page')
        transaction.commit()
        self._auth()
        self.browser.open(self.portal_url + '/' + _id)
        self.assertIn('template-simplelayout', self.browser.contents)
        self.assertIn('simplelayout-content', self.browser.contents)

    def tearDown(self):
        super(TestPageCreation, self).tearDown()
