from Acquisition import aq_inner, aq_parent
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import logout
from plone.app.testing import setRoles, login
from simplelayout.base.interfaces import IOneColumn
from simplelayout.base.interfaces import ISimpleLayoutBlock
from simplelayout.base.interfaces import ISimplelayoutView
from simplelayout.base.interfaces import ISlotA
from simplelayout.base.interfaces import ISlotB
from simplelayout.base.interfaces import ISlotD
from simplelayout.base.testing import SL_TYPES_INTEGRATION_TESTING
from unittest2 import TestCase
from zope.event import notify
from zope.interface import alsoProvides
from zope.interface import noLongerProvides
from zope.lifecycleevent import ObjectMovedEvent


class TestHandlers(TestCase):

    layer = SL_TYPES_INTEGRATION_TESTING

    def setUp(self):
        super(TestHandlers, self).setUp()
        self.portal = self.layer['portal']
        self.portal_url = self.portal.portal_url()

        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        login(self.portal, TEST_USER_NAME)

        self.folder = self.portal.get(
            self.portal.invokeFactory('Folder', 'testfolder'))
        self.folder.processForm()

        self.subfolder = self.folder.get(
            self.folder.invokeFactory('Folder', 'subfolder'))
        self.subfolder.processForm()

        self.page = self.folder.get(
            self.folder.invokeFactory('Page', 'page1'))
        self.page.processForm()

        self.page2 = self.folder.get(
            self.folder.invokeFactory('Page', 'page2'))
        self.page2.processForm()

        self.paragraph = self.page.get(
            self.page.invokeFactory('Paragraph', 'p1'))
        self.paragraph.processForm()

    def tearDown(self):
        self.portal.manage_delObjects(['testfolder'])
        logout()
        setRoles(self.portal, TEST_USER_ID, ['Member'])
        super(TestHandlers, self).tearDown()

    def test_block_moving(self):
        alsoProvides(
            self.paragraph,
            [ISimpleLayoutBlock, ISlotB, ISlotD])

        alsoProvides(self.page2, ISimplelayoutView)

        notify(ObjectMovedEvent(
                self.paragraph,
                self.page, 'p1',
                self.page2, 'p2'))

        # old slot interfaces are no longer provided
        self.assertFalse(ISlotB.providedBy(self.paragraph))
        self.assertFalse(ISlotD.providedBy(self.paragraph))

        # current view config interfaces should be provided
        self.assertTrue(ISlotA.providedBy(self.paragraph))
        self.assertTrue(IOneColumn.providedBy(self.paragraph))

    def test_page_moving(self):
        noLongerProvides(self.paragraph, ISlotA)
        alsoProvides(self.paragraph, ISlotB)

        self.assertFalse(ISlotA.providedBy(self.paragraph))
        self.assertTrue(ISlotB.providedBy(self.paragraph))

        self.assertEqual(aq_parent(aq_inner(self.page)).getId(), 'testfolder')
        cutted = self.folder.manage_cutObjects([self.page.getId()])
        self.subfolder.manage_pasteObjects(cutted)

        page = self.subfolder.get('page1')
        paragraph = page.get('p1')
        self.assertEqual(aq_parent(aq_inner(page)).getId(), 'subfolder')

        # The paragraph should not be changed, since we move the page.
        self.assertFalse(ISlotA.providedBy(paragraph))
        self.assertTrue(ISlotB.providedBy(paragraph))

    def test_page_copy(self):
        noLongerProvides(self.paragraph, ISlotA)
        alsoProvides(self.paragraph, ISlotB)

        self.assertFalse(ISlotA.providedBy(self.paragraph))
        self.assertTrue(ISlotB.providedBy(self.paragraph))

        self.assertEqual(aq_parent(aq_inner(self.page)).getId(), 'testfolder')
        copied = self.folder.manage_copyObjects([self.page.getId()])
        self.subfolder.manage_pasteObjects(copied)

        page = self.subfolder.get('page1')
        paragraph = page.get('p1')
        self.assertEqual(aq_parent(aq_inner(page)).getId(), 'subfolder')

        # The paragraph should not be changed, since we move the page.
        self.assertFalse(ISlotA.providedBy(paragraph))
        self.assertTrue(ISlotB.providedBy(paragraph))
