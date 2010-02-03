from zope.component import getUtility, getMultiAdapter
from Products.CMFCore.utils import getToolByName
from simplelayout.base.utils import IBlockControl
from simplelayout.base.interfaces import IScaleImage, IBlockConfig, ISlUtils
from simplelayout.base.interfaces import ISimplelayoutView, ISimpleLayoutCapable
from simplelayout.base.config import INIT_INTERFACES_MAP,VIEW_INTERFACES_MAP
from zope.interface import providedBy, alsoProvides
from DateTime import DateTime

def isWorkflowEnabled():
    conf = getUtility(ISlUtils, name='simplelayout.utils')
    return conf.isBlockWorkflowEnabled()    


def set_initial_layout(object, event):
    content = event.object
    parent = content.aq_parent
    
    if not ISimpleLayoutCapable.providedBy(parent):
        return
    
    blockconf = IBlockConfig(content)

    types_tool = getToolByName(content, 'portal_types')
    actions = types_tool.listActions(object=content)  
    category =  'sl-layouts'
    #we use the the first layout as default value
    layout = blockconf.image_layout
    viewname = blockconf.viewname
    if not layout:
        for action in actions:
            if action.category == category:
                layout = action.id
                #XXX refactor me
                #bit nasty. it removes "sl-"
                layout = layout[3:]
                break
    if layout:
        converter = getUtility(IBlockControl, name='block-layout')
        converter.update(content, content, content.REQUEST, layout=layout, viewname=viewname)
        
def changeBlockStates(obj, event):
    """
    """
    if not ISimpleLayoutCapable.providedBy(obj):
        return
    
    if not isWorkflowEnabled():
        pm = getToolByName(obj, 'portal_membership')
        current_user = pm.getAuthenticatedMember().getId()
        wt = getToolByName(obj, 'portal_workflow')
        wf_id = wt.getChainFor(obj)[0]
        container_status = wt.getInfoFor(obj, 'review_state')
        cf = {'object_provides': 'simplelayout.base.interfaces.ISimpleLayoutBlock'}
        comment = 'state set to: %s' % container_status
        for item in obj.getFolderContents(cf, full_objects=True):
            wt.setStatusOf(wf_id, item, {'review_state': container_status,
                                         'action' : container_status, 
                                         'actor': current_user,
                                         'time': DateTime(),
                                         'comments': comment,})
            wf = wt.getWorkflowById(wf_id)
            wf.updateRoleMappingsFor(item)
            item.reindexObject(idxs=['allowRolesAndUsers', 'review_state'])


def changeBlockStateToSameAsParent(obj,event):
    """
    """
    parent = obj.aq_parent
    if not ISimpleLayoutCapable.providedBy(parent):
        return
        
    if not isWorkflowEnabled():
        pm = getToolByName(obj, 'portal_membership')
        current_user = pm.getAuthenticatedMember().getId()
        wt = getToolByName(obj, 'portal_workflow')
        wf_id = wt.getChainFor(obj)[0]
        container_status = wt.getInfoFor(obj.aq_inner.aq_parent, 'review_state')
        comment = 'state set to: %s' % container_status
        wt.setStatusOf(wf_id, obj, {'review_state': container_status,
                                         'action' : container_status, 
                                         'actor': current_user,
                                         'time': DateTime(),
                                         'comments': comment,})
        wf = wt.getWorkflowById(wf_id)
        wf.updateRoleMappingsFor(obj)
        obj.reindexObject(idxs=['allowRolesAndUsers', 'review_state'])  


def setDefaultDesignInterface(obj,event):
    if not ISimplelayoutView.providedBy(obj):
        alsoProvides(obj, ISimplelayoutView)
    
def setDefaultBlockInterfaces(obj,event):
    parent = obj.aq_parent
    parent_iface = None
    for i in VIEW_INTERFACES_MAP.values():
        if i.providedBy(parent):
            parent_iface = i
    
    if parent_iface is None:
        return 
    name = parent_iface['name'].__name__     
    ifaces = []
    if INIT_INTERFACES_MAP.has_key(name):
        ifaces = INIT_INTERFACES_MAP[name]
    for iface in ifaces: alsoProvides(obj, iface)
    obj.reindexObject(idxs=['object_provides'])
    
    #XXX this should be done earlier, we do now twice... once is enought
    #calc new images sizes and store them
    try:
        converter = getUtility(IBlockControl, name='block-layout')
    except ComponentLookupError:
        pass
    converter.update(parent, obj, obj.REQUEST) 

