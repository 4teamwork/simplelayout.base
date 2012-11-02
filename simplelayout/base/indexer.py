from simplelayout.base.config import BLOCK_INTERFACES
from zope.component import getUtility
from simplelayout.base.interfaces import ISlUtils
from plone.indexer import indexer
from simplelayout.base.interfaces import ISimpleLayoutCapable


@indexer(ISimpleLayoutCapable)
def SearchableText(obj):
    searchable_text = obj.SearchableText()
    # only index sub-blocks if blockworkflow is not enabled
    conf = getUtility(ISlUtils, name='simplelayout.utils')
    if not conf.isBlockWorkflowEnabled():
        contents = obj.getFolderContents(
            {'object_provides': BLOCK_INTERFACES,
             'sort_order': 'getObjPositionInParent'},
            full_objects=True)
        for content in contents:
            # do not add SearchableText if content is a file
            if content.portal_type != 'File':
                searchable_text += content.SearchableText()
        if isinstance(searchable_text, unicode):
            searchable_text = searchable_text.encode('utf8')
    return searchable_text
