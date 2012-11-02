from plone.app.testing import setRoles, login
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME, TEST_USER_PASSWORD
from plone.testing.z2 import Browser
from simplelayout.base.interfaces import ISimpleLayoutBlock
from simplelayout.base.testing import SL_BASE_INTEGRATION_TESTING
from unittest2 import TestCase
import transaction


class TestParagraphCreation(TestCase):

    layer = SL_BASE_INTEGRATION_TESTING

    def setUp(self):
        super(TestParagraphCreation, self).setUp()
        self.portal = self.layer['portal']
        self.portal_url = self.portal.portal_url()

        self.page = self.portal.get(
            self.portal.invokeFactory('Page', 'slpage'))
        self.page.processForm()
        transaction.commit()

        # Browser setup
        self.browser = Browser(self.layer['app'])
        self.browser.handleErrors = False
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        login(self.portal, TEST_USER_NAME)

    def _auth(self):
        self.browser.addHeader('Authorization', 'Basic %s:%s' % (
                TEST_USER_NAME, TEST_USER_PASSWORD, ))

    def test_fti(self):
        self.assertIn('Paragraph', self.portal.portal_types.objectIds())

    def test_creation(self):
        _id = self.page.invokeFactory('Paragraph', 'paragraph')
        self.assertIn(_id, self.page.objectIds())

    def test_block_marker_interface(self):
        block = self.page.get(
            self.page.invokeFactory('Paragraph', 'paragraph'))
        ISimpleLayoutBlock.providedBy(block)

    def test_simplelayout_view(self):
        self._auth()
        self.browser.open("%s/createObject?type_name=Paragraph" %
            self.page.absolute_url())
        self.browser.getControl(name='text').value = 'DUMMY-TEXT'
        self.browser.getControl('Save').click()
        self.browser.open(self.page.absolute_url())
        self.assertIn('BlockOverallWrapper', self.browser.contents)
        self.assertIn('DUMMY-TEXT', self.browser.contents)
        self.assertIn('template-simplelayout', self.browser.contents)
        self.assertIn(self.page.objectValues()[0].UID(), self.browser.contents)

    def tearDown(self):
        super(TestParagraphCreation, self).tearDown()
        portal = self.layer['portal']
        portal.manage_delObjects(['slpage'])
        transaction.commit()
