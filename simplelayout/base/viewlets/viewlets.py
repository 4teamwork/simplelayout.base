from zope.interface import implements, alsoProvides
from plone.app.layout.viewlets import ViewletBase
from zope.component import getMultiAdapter
import zope.component
from zope.component import getUtility
from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName
from zope.contentprovider import interfaces as cp_interfaces
from zope.component.exceptions import ComponentLookupError
from zope.contentprovider.tales import addTALNamespaceData
from plone.memoize import instance,view
from plone.memoize import view, ram
from plone.app.layout.viewlets.content import DocumentActionsViewlet
from plone.app.layout.globals.interfaces import IViewView 

from simplelayout.base import config
from simplelayout.base.interfaces import ISimpleLayoutListingViewlet,  \
                                         ISimpleLayoutListingTwoColumnsViewlet, \
                                         ISimpleLayoutListingTwoColumnsOneOnTopViewlet, \
                                         IBlockConfig, \
                                         IScaleImage, \
                                         ISimpleLayoutBlock, \
                                         ISlUtils
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.Expression import getExprContext
from zope.i18n import translate

#dummy for refactoring
_ = lambda x: x

def _checkForEditMode(context):
    edit_mode = False
    if context.REQUEST.get('edit_mode',False):
        edit_mode = True
    if context.REQUEST.get('HTTP_REFERER', 'dummytext_longer_as_five_chars')[-5:] == '/edit':
        edit_mode = True
    return edit_mode


class SimpleLayoutListingViewlet(ViewletBase):
    render = ViewPageTemplateFile('listing.pt')
    implements(ISimpleLayoutListingViewlet)
    
    def getSimpleLayoutContents(self, slotInterface=''):
        if self.context.isPrincipiaFolderish:
            if config.SLOT_INTERFACES_MAP.has_key(slotInterface):
                slotInterface = [config.SLOT_INTERFACES_MAP[slotInterface].__identifier__]
            else:
                slotInterface = []
            return self.context.getFolderContents({'object_provides':{'query':config.BLOCK_INTERFACES + slotInterface,'operator': 'and'},
                                                   'sort_order':'getObjPositionInParent'
                                                   }, 
                                                  full_objects=True)



        #this part is used for the plone default versioning function
        else:
            return [self.context]
    
    def renderBlockProvider(self, context):    
        view = self
        block = context
        request = self.request
        
        blockconf = IBlockConfig(context)
        name = blockconf.viewlet_manager

        #Paragraph is our example, this content type has no ViewletManager
        #so it should use simplelayout.base.block
        default = 'block'
        prefix = 'simplelayout.base'
        #first time we have to generate the viewletManager name.
        #so we have the possibility to change the manager later. 
        if name is None:

            #now build the viewletManager name from given prefix and 
            #block.__class__.__name__ (ClassName)
            name = '%s.%s' % (prefix, block.__class__.__name__)
            blockconf.viewlet_manager = name
    
        provider = None
        counter = 0
        while provider is None and counter < 10:
            provider = zope.component.queryMultiAdapter(
                (block, request, view), cp_interfaces.IContentProvider, name)
            counter +=1
            if provider is None:
                name = '%s.%s' % (prefix,default)


        #if provider is still None
        if provider is None:
            return 'Something is wrong - pls debug'

        addTALNamespaceData(provider, block)
        provider.update()
        return provider.render()
        
    def UserHasPermission(self):
        portal_state = getMultiAdapter((self.context, self.request),
                                            name=u'plone_portal_state')
                                          
        member = portal_state.member()
        return member.has_permission('Add portal_content',self.context)
        
    def checkForEditMode(self):
        return _checkForEditMode(self.context)

    def getWrapperCss(self,context):
        blockconf = IBlockConfig(context)
        normalize = getMultiAdapter((context, self.request), name='plone').normalizeString
        additional_css_class = normalize(context.Type())
        layout = blockconf.image_layout
        if layout is None:
            return additional_css_class + ' BlockWrapper-no-image' 
        cssclass = additional_css_class + ' BlockWrapper-'+layout
        return cssclass
        

class SimpleLayoutListingTwoColumnsViewlet(SimpleLayoutListingViewlet):
    render = ViewPageTemplateFile('listing_two_columns.pt')
    implements(ISimpleLayoutListingTwoColumnsViewlet)
    
class SimpleLayoutListingTwoColumnsOneOnTopViewlet(SimpleLayoutListingViewlet):
    render = ViewPageTemplateFile('listing_two_columns_one_on_top.pt')
    implements(ISimpleLayoutListingTwoColumnsOneOnTopViewlet)


class SimpleLayoutControlsViewlet(ViewletBase):
    render = ViewPageTemplateFile('controls.pt')
    
    def getActions(self, category='sl-actions'):
        types_tool = getToolByName(self.context, 'portal_types')
        ai_tool = getToolByName(self.context, 'portal_actionicons')
        actions = types_tool.listActions(object=self.context)   
        for action in actions:
            if action.category == category:
                icon = ai_tool.queryActionIcon(action_id=action.id, category=category, context=self.context)
                econtext = getExprContext(self.context, self.context)
                action = action.getAction(ec=econtext)
                
                yield {
                       'id':action['id'],
                       'icon':icon,
                       'url':action['url']
                       }

    def getLayouts(self, category='sl-layouts'):
        return self.getActions(category)

    def getCurrentLayout(self,block):
        if ISimpleLayoutBlock.providedBy(block):
            blockconf = IBlockConfig(block)
            return blockconf.image_layout

        return None

    def checkForEditMode(self):
        return _checkForEditMode(self.context)
        
    def isWorkflowEnabled(self):
        conf = getUtility(ISlUtils, name='simplelayout.utils')
        return conf.isBlockWorkflowEnabled()        

class SimpleLayoutContentViewlet(ViewletBase):
    
    template = ViewPageTemplateFile('renderer.pt')
    render_fallback = ViewPageTemplateFile('fallback.pt')
    
    def render(self):
        self.block_view = None
        context = self.context.aq_explicit
        
        #TODO allow views for every layout
        #layout_name = 'listing'
        #block_view = zope.component.queryMultiAdapter((context, self.request), name='block_view-%s' % layout_name)
        if not self.block_view:
            self.block_view = zope.component.queryMultiAdapter((context, self.request), name='block_view')
            
        if self.block_view:
            return self.template()
        return self.render_fallback()
    
