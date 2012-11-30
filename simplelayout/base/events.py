from Acquisition import aq_parent, aq_inner
from DateTime import DateTime
from Products.CMFCore.utils import getToolByName
from simplelayout.base.config import INIT_INTERFACES_MAP
from simplelayout.base.config import SLOT_INTERFACES_MAP
from simplelayout.base.config import VIEW_INTERFACES_MAP
from simplelayout.base.interfaces import IBlockConfig, ISlUtils
from simplelayout.base.interfaces import ISimpleLayoutCapable
from simplelayout.base.interfaces import ISimplelayoutView
from simplelayout.base.utils import IBlockControl
from zope.component import getUtility
from zope.interface import noLongerProvides
from zope.component.interfaces import ComponentLookupError
from zope.interface import alsoProvides
import logging


LOG = logging.getLogger('simplelayout.base')


def isWorkflowEnabled():
    conf = getUtility(ISlUtils, name='simplelayout.utils')
    return conf.isBlockWorkflowEnabled()


def set_initial_layout(obj, event):
    content = event.object
    parent = content.aq_parent

    if not ISimpleLayoutCapable.providedBy(parent):
        return

    blockconf = IBlockConfig(content)

    types_tool = getToolByName(content, 'portal_types')
    actions = types_tool.listActions(object=content)
    category = 'sl-layouts'
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
        converter.update(content, content, content.REQUEST, layout=layout,
                         viewname=viewname)


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
        cf = {'object_provides':
                  'simplelayout.base.interfaces.ISimpleLayoutBlock'}
        comment = 'state set to: %s' % container_status
        for item in obj.getFolderContents(cf, full_objects=True):
            wt.setStatusOf(wf_id, item, {'review_state': container_status,
                                         'action': container_status,
                                         'actor': current_user,
                                         'time': DateTime(),
                                         'comments': comment,
                                         })
            wf = wt.getWorkflowById(wf_id)
            wf.updateRoleMappingsFor(item)
            item.reindexObject(idxs=['allowRolesAndUsers', 'review_state'])


def changeBlockStateToSameAsParent(obj, event):
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
        container_status = wt.getInfoFor(obj.aq_inner.aq_parent,
                                         'review_state')
        comment = 'state set to: %s' % container_status
        wt.setStatusOf(wf_id, obj, {'review_state': container_status,
                                         'action': container_status,
                                         'actor': current_user,
                                         'time': DateTime(),
                                         'comments': comment,
                                    })
        wf = wt.getWorkflowById(wf_id)
        wf.updateRoleMappingsFor(obj)
        obj.reindexObject(idxs=['allowRolesAndUsers', 'review_state'])


def setDefaultDesignInterface(obj, event):
    if not ISimplelayoutView.providedBy(obj):
        alsoProvides(obj, ISimplelayoutView)


def setDefaultBlockInterfaces(obj, event):
    parent = obj.aq_parent
    parent_iface = None
    for i in VIEW_INTERFACES_MAP.values():
        if i.providedBy(parent):
            parent_iface = i

    if parent_iface is None:
        return
    name = parent_iface['name'].__name__
    ifaces = []
    if name in INIT_INTERFACES_MAP:
        ifaces = INIT_INTERFACES_MAP[name]
    for iface in ifaces:
        alsoProvides(obj, iface)
    obj.reindexObject(idxs=['object_provides'])

    #XXX this should be done earlier, we do now twice... once is enought
    #calc new images sizes and store them
    try:
        converter = getUtility(IBlockControl, name='block-layout')
    except ComponentLookupError:
        pass
    converter.update(parent, obj, obj.REQUEST)


def reindexContainer(obj, event, parent=None):
    try:
        workflow_enabled = isWorkflowEnabled()
    except ComponentLookupError:
        # This happens when the plone site is removed.
        # In this case persistent utilites are already gone.
        # Reindexing is not necessary in this situation, since
        # everything will be gone.
        LOG.error('events.blockMoved() threw', exc_info=True)
        return

    if not workflow_enabled:
        if not parent:
            parent = aq_parent(aq_inner(obj))

        if not ISimpleLayoutCapable.providedBy(parent):
            return

        catalog = getToolByName(obj, 'portal_catalog')
        # Only reindex existing brains! The parent may be just
        # deleted, we should not put it back in the catalog.
        parent_path = '/'.join(parent.getPhysicalPath())
        if catalog.getrid(parent_path) is not None:
            parent.reindexObject()


def blockMoved(obj, event):
    reindexContainer(obj, event, parent=event.oldParent)
    reindexContainer(obj, event, parent=event.newParent)

    # remove slote interfaces
    for key, iface in SLOT_INTERFACES_MAP.items():
        if iface.providedBy(obj):
            noLongerProvides(obj, iface)

    # set current view config interfaces (slot and colum interface)
    for name, iface in VIEW_INTERFACES_MAP.items():
        if iface.providedBy(event.newParent):
            alsoProvides(obj, INIT_INTERFACES_MAP.get(name))
            break
