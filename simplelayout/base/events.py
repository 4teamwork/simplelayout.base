from Acquisition import aq_parent, aq_inner
from Products.CMFCore.utils import getToolByName
from simplelayout.base.config import INIT_INTERFACES_MAP
from simplelayout.base.config import SLOT_INTERFACES_MAP
from simplelayout.base.config import VIEW_INTERFACES_MAP
from simplelayout.base.interfaces import IBlockConfig
from simplelayout.base.interfaces import ISimpleLayoutCapable
from simplelayout.base.interfaces import ISimplelayoutView
from simplelayout.base.utils import IBlockControl
from zope.component import getUtility
from zope.interface import noLongerProvides
from zope.component.interfaces import ComponentLookupError
from zope.interface import alsoProvides
import logging


LOG = logging.getLogger('simplelayout.base')


def set_initial_layout(obj, event):
    content = event.object

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

    if obj != event.object:
        # Moving the parent, so we do not reset the layout.
        return

    # remove slote interfaces
    for key, iface in SLOT_INTERFACES_MAP.items():
        if iface.providedBy(obj):
            noLongerProvides(obj, iface)

    # set current view config interfaces (slot and colum interface)
    for name, iface in VIEW_INTERFACES_MAP.items():
        if iface.providedBy(event.newParent):
            alsoProvides(obj, INIT_INTERFACES_MAP.get(name))
            break
