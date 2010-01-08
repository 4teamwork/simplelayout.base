from zope.interface import Interface
from zope.app.publisher.interfaces.browser import IBrowserMenu
from zope.app.publisher.interfaces.browser import IBrowserSubMenuItem
from plone.app.contentmenu.view import ContentMenuProvider
from plone.app.contentmenu.interfaces import IContentMenuView
from plone.app.contentmenu import menu

from zope.app.publisher.browser.menu import BrowserMenu
from zope.app.publisher.browser.menu import BrowserSubMenuItem
from zope.app.component.hooks import getSite
from Acquisition import aq_inner, aq_base
from Products.CMFPlone import utils
from zope.component import getMultiAdapter, queryMultiAdapter, getAdapters, queryUtility,getUtility
from zope.interface import implements
from Products.CMFCore.utils import getToolByName
from plone.memoize.instance import memoize
from simplelayout.base.interfaces import ISlUtils, ISimpleLayoutCapable


from Products.CMFPlone import PloneMessageFactory as _

class IBlockDesignSubMenu(IBrowserSubMenuItem):
    """The menu item linking to the help menu.
    """

class IBlockDesignMenu(IBrowserMenu):
    """The help menu
    """

class BlockDesignSubMenu(BrowserSubMenuItem):
    implements(IBlockDesignSubMenu)
    
    title = _(u'label_design_menu', default=u'Design')
    description = _(u'desc_design_menu', default=u'change design of current page')
    submenuId = 'simplelayout_contentmenu_design'
    
    order = 5
    extra = {'id' : 'simplelayout-contentmenu-design'}
    
    def __init__(self, context, request):
        BrowserSubMenuItem.__init__(self, context, request)
        self.context_state = getMultiAdapter((context, request), name='plone_context_state')
    
    def getToolByName(self, tool):
        return getToolByName(getSite(), tool)

    @property
    def action(self):
        folder = self.context
        if not self.context_state.is_structural_folder():
            folder = utils.parent(self.context)
        return folder.absolute_url() + '/folder_contents'
    
    @memoize
    def available(self):
        
        conf = getUtility(ISlUtils, name='simplelayout.utils')
       
        context_state = getMultiAdapter((self.context, self.request),name=u'plone_context_state')
        sl_design_actions = context_state.actions().get('object_simplelayout_designs', [])
        return len(sl_design_actions) > 0 and conf.isDesignTabEnabled() and ISimpleLayoutCapable.providedBy(self.context)

    def selected(self):
        return False

class BlockDesignMenu(BrowserMenu):
    implements(IBlockDesignMenu)
    
    def getMenuItems(self, context, request):
        """Return menu item entries in a TAL-friendly form."""
        results = []

        portal_state = getMultiAdapter((context, request), name='plone_portal_state')

        context_state = getMultiAdapter((context, request),name=u'plone_context_state')
        sl_design_actions = context_state.actions().get('object_simplelayout_designs', [])

        if not sl_design_actions:
            return []

        plone_utils = getToolByName(context, 'plone_utils')
        portal_url = portal_state.portal_url()
        
        
        for action in sl_design_actions:
                cssClass = 'actionicon-help-%s' % action['id']

                results.append({ 'title'        : action['title'],
                                 'description'  : '',
                                 'action'       : action['url'],
                                 'selected'     : False,
                                 'icon'         : None,
                                 'extra'        : {'id' : action['id'], 'separator' : None},
                                 'submenu'      : None,
                                 })

        return results




class BlockWorkflowMenu(ContentMenuProvider):
    """Content menu provider for block workflow changes
    """
    
    implements(IContentMenuView)
        
    def menu(self):
        menu = getUtility(IBrowserMenu, name='plone_contentmenu')
        items = menu.getMenuItems(self.context, self.request)
        
        # copied from bernarticle.core.
        items = [item for item in items if item['title']=='label_state']
        
        for item in items:
            extra = item.get('extra')
            extra['id'] = '%s-%s' % (extra.get('id'), self.context.getId())
            item['extra'] = extra
            
        return items
  	 
