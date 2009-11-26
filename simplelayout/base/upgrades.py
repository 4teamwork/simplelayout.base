from Products.CMFCore.utils import getToolByName
import transaction
from zope.interface import providedBy, alsoProvides

from simplelayout.base.interfaces  import IBlockConfig
from simplelayout.base.config import BLOCK_INTERFACES
from simplelayout.base.interfaces import ISimpleLayoutBlock
        

from Acquisition import aq_inner
from Products.Archetypes.Storage import AttributeStorage
from simplelayout.base.config import VIEW_INTERFACES_MAP, \
                                    SLOT_INTERFACES_MAP, \
                                    COLUMN_INTERFACES_MAP, \
                                    BLOCK_INTERFACES


def migrateActionsAndLayoutNames(portal_setup):
    portal_url = getToolByName(portal_setup, 'portal_url')
    portal = portal_url.getPortalObject()
    catalog = getToolByName(portal_setup, 'portal_catalog')
    query = {}
    query['portal_type'] = ['Image', 'Paragraph']
    results = catalog(query)
    for b in results:
        obj = aq_inner(b.getObject()).aq_explicit
        blockconf = IBlockConfig(obj)
        layout = blockconf.image_layout
        migrate_layout = {'half':'middle',
                      'squarish':'small',
                      'full': 'full', 
                      'thumbnail':'small',
                      '25':'small',
                      '33':'middle',
                      '50':'full',
                      'no-image':'no-image'}
        if layout and layout not in ['small','middle','full']:
            blockconf.image_layout = migrate_layout[layout]


    newactionset = []
    obsoleteactions = ['sl-25','sl-33','sl-50','sl-squarish']
    image_actions = portal.portal_types.Image._cloneActions()
    for a in image_actions:
        if a.id in obsoleteactions:
            image_actions.remove(a)
    portal.portal_types.Image._actions = image_actions
    
    return 'migration done'
    
def set_block_states(portal_setup):
    containers = [c.getObject() for c in portal_setup.portal_catalog(object_provides='simplelayout.base.interfaces.ISimpleLayoutCapable')]
    wt = getToolByName(portal_setup, 'portal_workflow')
    
    for obj in containers:
        wf_id = wt.getChainFor(obj)[0]
        container_status = wt.getInfoFor(obj, 'review_state')
        cf = {'object_provides': 'simplelayout.base.interfaces.ISimpleLayoutBlock'}
    
        for item in obj.getFolderContents(cf, full_objects=True):
            wt.setStatusOf(wf_id, item, {'review_state': container_status})
            wf = wt.getWorkflowById(wf_id)
            wf.updateRoleMappingsFor(item)
            item.reindexObject(idxs=['allowRolesAndUsers', 'review_state'])

    return "Status of contained objects changed"
  

#set default interfaces, so the "normal" will work correctly    
def set_content_interfaces(portal_setup):
    catalog = portal_setup.portal_catalog
    containers = [c.getObject() for c in portal_setup.portal_catalog(object_provides='simplelayout.base.interfaces.ISimpleLayoutCapable')]
    iface = VIEW_INTERFACES_MAP['normal']
    for obj in containers:
        if not iface.providedBy(obj):
            alsoProvides(obj, iface)
            obj.reindexObject(idxs=['object_provides'])


    blocks = [c.getObject() for c in portal_setup.portal_catalog(object_provides=BLOCK_INTERFACES)]
    for obj in blocks:
        slot_iface = SLOT_INTERFACES_MAP['slotA']
        column_iface = COLUMN_INTERFACES_MAP['onecolumn']
        
        if not slot_iface.providedBy(obj):
            alsoProvides(obj,slot_iface)
        if not column_iface.providedBy(obj):
            alsoProvides(obj,column_iface)
        
        obj.reindexObject(idxs=['object_provides'])


def remove_unused_actions(portal_setup):
    """
    removes sl-edit-button and more unused actions
    """
    types = portal_setup.portal_types
    
    #remove sl-toggle action from Page
    page = types.Page
    tmplist = list(page._actions)
    to_remove = None
    for action in tmplist:
        if action.id == 'edit-toggle':
            to_remove = action
    if to_remove is not None:
        tmplist.remove(to_remove)
        page._actions = tuple(tmplist)


    #remove sl-up and sl-down actions from block types
    actions_to_remove = ['sl-moveup', 'sl-movedo']
    block_types = ['Paragraph', 'Link', 'Image', 'File',]
    for bt in block_types:
        if bt not in types.keys():
            continue
        dvti = types[bt]
        bt_actions = list(dvti._actions)
        for action in bt_actions:
            if action.id in actions_to_remove:
                bt_actions.remove(action)
        dvti._actions = tuple(bt_actions)
        
    return "Simplelayout Actions migrated"
