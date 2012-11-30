from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import setRoles, login
from simplelayout.base.interfaces import IOneColumn
from simplelayout.base.interfaces import ISimpleLayoutBlock
from simplelayout.base.interfaces import ISimplelayoutView
from simplelayout.base.interfaces import ISlotA
from simplelayout.base.interfaces import ISlotB
from simplelayout.base.interfaces import ISlotD
from simplelayout.base.testing import SL_BASE_INTEGRATION_TESTING
from unittest2 import TestCase
from zope.event import notify
from zope.interface import alsoProvides
from zope.lifecycleevent import ObjectMovedEvent


class TestHandlers(TestCase):

    layer = SL_BASE_INTEGRATION_TESTING

    def setUp(self):
        super(TestHandlers, self).setUp()
        self.portal = self.layer['portal']
        self.portal_url = self.portal.portal_url()

        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        login(self.portal, TEST_USER_NAME)

        self.page = self.portal.get(
            self.portal.invokeFactory('Page', 'page1'))
        self.page2 = self.portal.get(
            self.portal.invokeFactory('Page', 'page2'))

        self.paragraph = self.page.get(
            self.page.invokeFactory('Paragraph', 'p1'))

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
