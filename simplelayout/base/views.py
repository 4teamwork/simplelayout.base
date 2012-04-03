from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName

import zope.component
from zope.interface import implements, alsoProvides, noLongerProvides
from zope.component import getUtility

from zope.contentprovider import interfaces as cp_interfaces
from zope.component.interfaces import ComponentLookupError

from zope.contentprovider.tales import addTALNamespaceData
from utils import IBlockControl
from Acquisition import aq_inner
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from simplelayout.base.interfaces import ISimplelayoutView, \
                                         ISimpleLayoutCapable
from simplelayout.base.config import VIEW_INTERFACES_MAP, \
                                     SLOT_INTERFACES_MAP, \
                                     COLUMN_INTERFACES_MAP, \
                                     BLOCK_INTERFACES, \
                                     INIT_INTERFACES_MAP

from simplelayout.base.interfaces import IBlockConfig

class SimpleLayoutView(BrowserView):
    implements(ISimplelayoutView)

    template = ViewPageTemplateFile('browser/simplelayout.pt')

    def __call__(self):
        return self.template()

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
        plone_properties = getToolByName(self.context, 'portal_properties')
        plonegov_properties = getattr(
            plone_properties,
            'plonegov.website_properties',
            False)
        use_types = plonegov_properties and getattr(
            plonegov_properties,
            'org_unit_list_types',
            []) or []

        return use_types

    def getContents(self):

        contentFilter = {'portal_type': self.getContentTypes(),
                         'sort_on': 'sortable_title'}
        return self.context.getFolderContents(contentFilter)

    def toggle_align_to_grid(self, new_value='1'):
        """
        toggles alignment to grid
        """
        context = aq_inner(self.context).aq_explicit
        if hasattr(context, 'align_to_grid'):
            self.context.manage_changeProperties({'align_to_grid': new_value})
        else:
            context.manage_addProperty('align_to_grid', new_value, 'string')

        return 1

    def isSimplelayout(self):
        """returns boolean if sl capable or not
        """
        context = self.context
        m_tool = getToolByName(context, 'portal_membership')
        capable = ISimpleLayoutCapable.providedBy(context)
        if m_tool.isAnonymousUser():
            return False
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

        if 'action' in self.request:
            name = 'action'
        if 'layout' in self.request:
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
            if hasattr(context_expl, 'align_to_grid'):
                context.manage_changeProperties({'align_to_grid': '0'})

            if name not in VIEW_INTERFACES_MAP:
                new = VIEW_INTERFACES_MAP['normal']
            else:
                new = VIEW_INTERFACES_MAP[name]
            #remove current design interface
            for iface in VIEW_INTERFACES_MAP.values():
                if iface.providedBy(context):
                    noLongerProvides(context, iface)
            #set the new one
            alsoProvides(context, new)
            context.reindexObject(idxs=['object_provides'])

        #set init interfaces on blocks
        ifaces = []
        if name in INIT_INTERFACES_MAP:
            ifaces = INIT_INTERFACES_MAP[name]

        contents = blocks and blocks or context.getFolderContents(
            {'object_provides': BLOCK_INTERFACES},
            full_objects=True)

        for obj in contents:
            #remove given block heights
            blockconf = IBlockConfig(obj)
            blockconf.block_height = None

            #remove all related Interfaces
            for i in COLUMN_INTERFACES_MAP.values()+ \
                SLOT_INTERFACES_MAP.values():

                if i.providedBy(obj):
                    noLongerProvides(obj, i)

            for iface in ifaces:
                alsoProvides(obj, iface)
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

    template = ViewPageTemplateFile("browser/controls.pt")

    def __call__(self):
        return self.template()


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

    def __call__(self):
        pass

    def setBlockHeights(self, uids=[], left=[], right=[]):
        """
        usage: needs a list of uid, height pairs...
        if the uid of a block is missing, the height attribute of this
        block will be deleted
        """
        # XXX:
        # Don't understand, why the varname:list, will shown as
        # varname:list[]
        # I just make this work, but i need to be fixed

        uids = self.request.get('uids:list[]', [])
        # In case if only one block is available
        if not isinstance(uids, list):
            uids = [uids]
        left = self.request.get('left:list[0][]', [])
        right = self.request.get('right:list[0][]', [])

        # create a dict
        _d = {}
        real_uids = [u.replace('uid_', '') for u in uids]

        if right or left:
            for uid, height in [right] + [left]:
                _d[uid.replace('uid_', '')] = height

        for uid in real_uids:
            block = self.context.reference_catalog.lookupObject(uid)
            blockconf = IBlockConfig(block)
            if uid in _d.keys():
                #set height
                blockconf.block_height = _d[uid]
            else:
                #remove heights
                blockconf.block_height = None

        return 1
