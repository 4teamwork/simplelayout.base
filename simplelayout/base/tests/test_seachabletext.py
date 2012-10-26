import transaction
from plone.app.testing import setRoles
from zope.component import getUtility
from simplelayout.base.interfaces import ISlUtils
from plone.app.testing import TEST_USER_ID
from Products.Archetypes.event import ObjectEditedEvent
from Products.CMFCore.utils import getToolByName
from simplelayout.base.indexer import SearchableText
from simplelayout.base.testing import SL_BASE_FUNCTIONAL_TESTING
from unittest2 import TestCase
from zope import event


class TestSearchableText(TestCase):

    layer = SL_BASE_FUNCTIONAL_TESTING

    def setUp(self):
        super(TestSearchableText, self).setUp()
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('Page', 'page1')

        self.page1 = self.portal.page1
        self.page1.invokeFactory('Paragraph', 'block1')
        self.page1.reindexObject()

        self.catalog = getToolByName(self.portal, 'portal_catalog')
        transaction.commit()

    def tearDown(self):
        super(TestSearchableText, self).tearDown()
        self.portal.manage_delObjects(['page1'])
        transaction.commit()

    def search_for(self, term, path=None):
        query = {'SearchableText': term, 'portal_type': 'Page'}
        if path:
            query['path'] = path
        return len(self.catalog(query))

    def test_blocks(self):
        self.assertEqual(SearchableText(self.page1)(), 'page1 block1 ')
        self.page1.invokeFactory('Paragraph', 'another')
        self.assertEqual(SearchableText(self.page1)(),
                         'page1 block1 another ')

    def test_block_deleted(self):
        # search for block
        self.assertTrue(self.search_for('block1') == 1)
        # delete object (manage_delObject fires event)
        self.page1.manage_delObjects(['block1'])
        self.assertTrue(self.search_for('block1') == 0)

    def test_block_edited(self):
        self.page1.block1.edit(description='lorem')
        event.notify(ObjectEditedEvent(self.page1.block1))
        self.assertTrue(self.search_for('lorem') == 1)

    def test_cut_paste(self):
        self.portal.invokeFactory('Page', 'p2')
        p2 = self.portal.p2
        page1_path = '/'.join(self.page1.getPhysicalPath())
        p2_path = '/'.join(p2.getPhysicalPath())

        self.assertTrue(self.search_for('block1', path=p2_path) == 0)
        self.assertTrue(self.search_for('block1', path=page1_path) == 1)

        #cut and paste
        transaction.commit()
        cookie = self.page1.manage_cutObjects(['block1'])
        transaction.commit()
        p2.manage_pasteObjects(cookie)
        transaction.commit()

        self.assertTrue(self.search_for('block1', path=p2_path) == 1)
        self.assertTrue(self.search_for('block1', path=page1_path) == 0)

    def test_umlauts(self):
        self.page1.block1.setDescription('utf8 \xc3\xa4')
        self.page1.invokeFactory('Paragraph', 'block2')
        self.page1.block2.setDescription(u'unicode \xfc')
        self.page1.reindexObject()
        self.assertEquals(self.search_for('\xc3\xa4'), 1)
        self.assertEquals(self.search_for('\xc3\xbc'), 1)

    def test_same_workflow(self):
        self.assertEqual(SearchableText(self.page1)(), 'page1 block1 ')
        conf = getUtility(ISlUtils, name='simplelayout.utils')
        ori_isBlockWorkflowEnabled = getattr(conf, 'isBlockWorkflowEnabled')
        setattr(conf, 'isBlockWorkflowEnabled', lambda: True)
        try:
            self.page1.reindexObject()
            self.assertEqual(SearchableText(self.page1)(), 'page1 ')
        finally:
            setattr(conf, 'isBlockWorkflowEnabled',
                    ori_isBlockWorkflowEnabled)
