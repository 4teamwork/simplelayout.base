from plone.app.content.browser import folderfactories
from plone.memoize.instance import memoize
from zope.component import getMultiAdapter

class SimplelayoutFactories(folderfactories.FolderFactoriesView):
    
    @memoize
    def add_context(self):
        context_state = getMultiAdapter((self.context, self.request), name='plone_context_state')
        if context_state.is_default_page() and context_state.is_folderish():
            return context_state.context
        return context_state.folder()
