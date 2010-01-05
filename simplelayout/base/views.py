from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName

import zope.component
from zope.interface import implements, providedBy, alsoProvides, noLongerProvides
from zope.component import getUtility, getMultiAdapter
from Products.CMFCore.utils import getToolByName

from zope.contentprovider import interfaces as cp_interfaces
from zope.component.exceptions import ComponentLookupError

from zope.contentprovider.tales import addTALNamespaceData
from utils import IBlockControl

from Acquisition import aq_inner

from plone.app.contentmenu.view import ContentMenuProvider
from plone.app.contentmenu.interfaces import IContentMenuView
from zope.app.publisher.interfaces.browser import IBrowserMenu
from simplelayout.base.interfaces import ISimplelayoutView, \
                                         ISimpleLayoutCapable
from simplelayout.base.config import VIEW_INTERFACES_MAP, \
                                     SLOT_INTERFACES_MAP, \
                                     COLUMN_INTERFACES_MAP, \
                                     BLOCK_INTERFACES, \
                                     INIT_INTERFACES_MAP


from Products.CMFCore.Expression import getExprContext

from simplelayout.base.interfaces import ISimpleLayoutListingViewlet,  \
                                      ISimplelayoutTwoColumnView, \
                                      ISimplelayoutTwoColumnOneOnTopView, \
                                      IBlockConfig, \
                                      IScaleImage, \
                                      ISimpleLayoutBlock, \
                                      ISlUtils

class SimpleLayoutView(BrowserView):
    implements(ISimplelayoutView)

    def getSimpleLayoutContents(self):
        results = self.context.getFolderContents()
        #XXX: use your brains...
        results = [result.getObject() for result in results]
        return results
    
    def renderBlockProvider(self, context):
        name = u'zug.simplelayout.block'
        context = context
        request = self.request
        view = self
        provider = zope.component.queryMultiAdapter(
            (context, request, view), cp_interfaces.IContentProvider, name)
        addTALNamespaceData(provider, context)
        provider.update()
        return provider.render()
        
    def getContentTypes(self):
        plone_properties = getToolByName(self.context,'portal_properties')
        plonegov_properties = getattr(plone_properties,'plonegov.website_properties',False)
        use_types = plonegov_properties and getattr(plonegov_properties,'org_unit_list_types',[]) or []
        
        return use_types 
    
    def getContents(self):

        contentFilter = {'portal_type':self.getContentTypes(),
                         'sort_on':'sortable_title'}
        return self.context.getFolderContents(contentFilter)

    def toggle_align_to_grid(self,new_value='1'):
        """
        toggles alignment to grid
        """
        context = aq_inner(self.context).aq_explicit

        if hasattr(context,'align_to_grid'):
            self.context.manage_changeProperties({'align_to_grid':new_value})
        else:
            context.manage_addProperty('align_to_grid',new_value,'string')
            
        return 1
            
    @property
    def isSimplelayout(self):
        """returns boolean if sl capable or not
        """
        context = self.context
        m_tool = getToolByName(context, 'portal_membership')
        capable = ISimpleLayoutCapable.providedBy(context)
        if m_tool.isAnonymousUser():return False
        member = m_tool.getAuthenticatedMember()
        # don't check modify permissions, cause edit is also in use in
        # other sircumstances
        return capable and member



class SimpleLayoutBlockView(BrowserView):  
    pass  
    
class BlockControl(BrowserView):
    
    def __call__(self):    
        parent = aq_inner(self.context).aq_parent
        response = self.request.response

        if self.request.has_key('action'):
            name = 'action'
        if self.request.has_key('layout'):
            name = 'layout'
        if name:
            utilname = 'block-'+name
            try:
                converter = getUtility(IBlockControl, 
                                       name=utilname)
            except ComponentLookupError:
                return response.redirect(parent.absolute_url())
    
            converter.update(parent, self.context, self.request)
        return response.redirect(parent.absolute_url())


class ChangeDesign(BrowserView):
    def __init__(self, context, request):
        self.context = context
        self.request = request 
    
    def setDesignInterface(self, name, blocks=[]):
        """ sets the new view interface """

        context = self.context
        context_expl = aq_inner(self.context).aq_explicit
        
        if not blocks:
            #remove grid infos
            if hasattr(context_expl,'align_to_grid'):
                context.manage_changeProperties({'align_to_grid':'0'})
                
            if not VIEW_INTERFACES_MAP.has_key(name):
                new = VIEW_INTERFACES_MAP['normal']
            else:
                new = VIEW_INTERFACES_MAP[name]
            #remove current design interface
            for iface in VIEW_INTERFACES_MAP.values():
                if iface.providedBy(context):
                    noLongerProvides(context, iface)
            #set the new one
            alsoProvides(context,new)
            context.reindexObject(idxs=['object_provides'])
        
        #set init interfaces on blocks
        ifaces = []
        if INIT_INTERFACES_MAP.has_key(name):
            ifaces = INIT_INTERFACES_MAP[name]
        
        contents = blocks and blocks or context.getFolderContents({'object_provides':BLOCK_INTERFACES}, full_objects=True)
        
        for obj in contents:
            #remove given block heights
            blockconf = IBlockConfig(obj)
            blockconf.block_height = None
            
            #remove all related Interfaces
            for i in COLUMN_INTERFACES_MAP.values()+SLOT_INTERFACES_MAP.values():
                if i.providedBy(obj): noLongerProvides(obj,i)
            for iface in ifaces: alsoProvides(obj, iface)
            obj.reindexObject(idxs=['object_provides'])

            #calc new images sizes and store them
            try:
                converter = getUtility(IBlockControl, name='block-layout')
            except ComponentLookupError:
                pass
            converter.update(context, obj, obj.REQUEST)
        
        if not blocks:
            return self.request.RESPONSE.redirect(context.absolute_url())
    
    
    
class SimpleLayoutControlsView(BrowserView):

    def getActions(self, category='sl-actions'):
        types_tool = getToolByName(self.context, 'portal_types')
        m_tool = getToolByName(self.context, 'portal_membership')
        ai_tool = getToolByName(self.context, 'portal_actionicons')
        actions = types_tool.listActions(object=self.context)
        member = m_tool.getAuthenticatedMember()
        for action in actions:
            has_permissions = True
            if action.category == category:
                for permission in action.permissions:
                    if not member.has_permission(permission, self.context):
                        has_permissions = False

                if not has_permissions:
                    continue
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
            viewname = blockconf.viewname
            image_layout = blockconf.image_layout
            if not image_layout: image_layout = ''
            if not viewname: viewname = ''
            if viewname: viewname = '-%s' % viewname
            return  image_layout + viewname

        return None

    def isWorkflowEnabled(self):
        conf = getUtility(ISlUtils, name='simplelayout.utils')
        return conf.isBlockWorkflowEnabled()    
        
    
    def isTwoColumnLayout(self):
        context = aq_inner(self.context).aq_explicit

        if ISimplelayoutTwoColumnView.providedBy(context):return True
        if ISimplelayoutTwoColumnOneOnTopView.providedBy(context):return True
        return False
        
    def ToggleGridLayoutText(self):
        """
        toggles align to grid text
        """
        context = context = aq_inner(self.context).aq_explicit
        align_to_grid_text = "Align blocks to grid"
        not_align_to_grid_text = "remove align to grid"
        grid = getattr(context.aq_inner.aq_explicit, 'align_to_grid', '0')
        return int(grid) and not_align_to_grid_text or align_to_grid_text

class BlockManipulation(BrowserView):
    """
    """

    def setBlockHeights(self, uids=[], left=[], right=[]):
        """
        usage: needs a list of uid, height pairs...
        if the uid of a block is missing, the height attribute of this 
        block will be deleted
        """
        # create a dict
        _d = {}
        real_uids = [u.replace('uid_','') for u in uids]
        both = [[l.split(',')[0],l.split(',')[1]] for l in left] + [[r.split(',')[0],r.split(',')[1]] for r in right]
        for uid,height in both:
            _d[uid.replace('uid_','')] = height
        
        
        for uid in real_uids:
            block = self.context.reference_catalog.lookupObject(uid)
            blockconf = IBlockConfig(block)
            if uid in _d.keys():
                #set height
                blockconf.block_height = _d[uid]
            else:
                #remove height
                blockconf.block_height = None
                
        return 1
