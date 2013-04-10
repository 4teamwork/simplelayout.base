from plone.indexer import indexer
from simplelayout.base.config import BLOCK_INTERFACES
from simplelayout.base.interfaces import ISimpleLayoutCapable
from zope.component import adapts


@indexer(ISimpleLayoutCapable)
def SearchableText(obj):
    searchable_text = obj.SearchableText()
    searchable_text += get_blocks_searchable_text(obj)
    return searchable_text


def get_blocks_searchable_text(obj):
    searchable_text = ''
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


class DexteritySearchableBlockTextExtender(object):
    adapts(ISimpleLayoutCapable)

    def __init__(self, context):
        self.context = context

    def __call__(self):
        return get_blocks_searchable_text(self.context)
