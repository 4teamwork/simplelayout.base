from Acquisition import aq_inner
from Products.CMFCore.ActionInformation import ActionInfo
from Products.CMFCore.utils import _checkPermission
from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets import ViewletBase
from simplelayout.base import config
from simplelayout.base.interfaces import IBlockConfig
from simplelayout.base.interfaces import ISimpleLayoutBlock
from simplelayout.base.interfaces import ISimpleLayoutListingTwoColumnsOneOnTopViewlet
from simplelayout.base.interfaces import ISimpleLayoutListingTwoColumnsViewlet
from simplelayout.base.interfaces import ISimpleLayoutListingViewlet
from simplelayout.base.interfaces import IAdditionalListingEnabledViewlet
from simplelayout.base.interfaces import ISimplelayoutTwoColumnOneOnTopView
from simplelayout.base.interfaces import ISimplelayoutTwoColumnView
from simplelayout.base.interfaces import ISlUtils
from zope.component import getMultiAdapter
from zope.component import getUtility
from zope.contentprovider import interfaces as cp_interfaces
from zope.contentprovider.tales import addTALNamespaceData
from zope.interface import implements
import logging
import zope.component
from plone.app.contentmenu.interfaces import IBrowserMenu


logger = logging.getLogger(__name__)

#dummy for refactoring
_ = lambda x: x


def _render_listing_cachkey(method, self, context):
    context_info = [context.modified, '/'.join(context.getPhysicalPath())]
    content_info = [(item.modified, item.getPath()) for item
                    in context.getFolderContents({
                'object_provides': config.BLOCK_INTERFACES})]
    return hash(tuple(context_info + content_info))


class SimpleLayoutListingViewlet(ViewletBase):
    render = ViewPageTemplateFile('listing.pt')
    implements(ISimpleLayoutListingViewlet)

    def getSimpleLayoutContents(self, slotInterface=''):
        if self.context.isPrincipiaFolderish:
            if slotInterface in config.SLOT_INTERFACES_MAP:
                slotInterface = [
                    config.SLOT_INTERFACES_MAP[slotInterface].__identifier__]
            else:
                slotInterface = []
            return self.context.getFolderContents(
                {'object_provides':
                     {'query': config.BLOCK_INTERFACES + slotInterface,
                      'operator': 'and'},
                 'sort_order': 'getObjPositionInParent'
                 }, full_objects=True)

        #this part is used for the plone default versioning function
        else:
            return [self.context]

    #XXX enable caching ASAP
    #@ram.cache(_render_listing_cachkey)
    def renderBlockProvider(self, context):
        #logger.info('sl viewlet renderer not cached')
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
            counter += 1
            if provider is None:
                name = '%s.%s' % (prefix, default)

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
        return member.has_permission('Add portal_content', self.context)

    def getWrapperCss(self, context):
        blockconf = IBlockConfig(context)
        normalize = getMultiAdapter((context, self.request),
                                    name='plone').normalizeString
        additional_css_class = normalize(context.Type())
        layout = blockconf.image_layout
        if layout is None:
            return additional_css_class + ' BlockWrapper-no-image'
        cssclass = additional_css_class + ' BlockWrapper-' + layout
        return cssclass


class SimpleLayoutListingTwoColumnsViewlet(SimpleLayoutListingViewlet):
    render = ViewPageTemplateFile('listing_two_columns.pt')
    implements(ISimpleLayoutListingTwoColumnsViewlet)


class SimpleLayoutListingTwoColumnsOneOnTopViewlet(SimpleLayoutListingViewlet):
    render = ViewPageTemplateFile('listing_two_columns_one_on_top.pt')
    implements(ISimpleLayoutListingTwoColumnsOneOnTopViewlet)


class AdditionalListingEnabledViewlet(SimpleLayoutListingViewlet):
    render = ViewPageTemplateFile('listing_additional.pt')
    implements(IAdditionalListingEnabledViewlet)


class SimpleLayoutControlsViewlet(ViewletBase):
    render = ViewPageTemplateFile('controls.pt')

    def getActions(self, category='sl-actions'):
        types_tool = getToolByName(self.context, 'portal_types')
        actions = types_tool.listActions(object=self.context)
        # Prepare actions
        ec = types_tool._getExprContext(self.context)
        actions = [ActionInfo(action, ec) for action in actions]

        for action in actions:

            if action['category'] == category and action['visible']:
                # Do not use action['allowed']
                # manually check permissions
                if not self._check_permission(action):
                    continue

                if not action['available']:
                    continue

                yield {
                    'id': action['id'],
                    'icon': action['icon'],
                    'title': action['title'],
                    'url': action['url']}

    def _check_permission(self, action):
        """Checks for the given permissions,
        because the one from plone is hard coded to several categories
        """
        for permission in action._permissions:
            if _checkPermission(permission, self.context):
                return True
        return False

    def getLayouts(self, category='sl-layouts'):
        return self.getActions(category)

    def getCurrentLayout(self, block):
        if ISimpleLayoutBlock.providedBy(block):
            blockconf = IBlockConfig(block)
            viewname = blockconf.viewname
            image_layout = blockconf.image_layout
            if not image_layout:
                image_layout = ''
            if not viewname:
                viewname = ''
            if viewname:
                viewname = '-%s' % viewname
            return  image_layout + viewname

        return None

    def _get_factory_menu(self):
        # Copied from factory menu tests
        if not getattr(self.context, 'isPrincipiaFolderish', False):
            return False
        else:
            # Also check for specific attribute
            show = getattr(self.context, 'showAddMenu', lambda: True)
            if show():
                menu = getUtility(
                    IBrowserMenu, name='plone_contentmenu',
                    context=self.context)
                items = menu.getMenuItems(self.context, self.request)
                factory_menu = [
                    i for i in items if
                    i['extra']['id'] == 'plone-contentmenu-factories'][0]
                factory_menu['extra']['id'] = 'sl-plone-contentmenu-factories'
                return factory_menu
            return False



class SimpleLayoutContentViewlet(ViewletBase):

    template = ViewPageTemplateFile('renderer.pt')
    render_fallback = ViewPageTemplateFile('fallback.pt')

    def render(self):
        context = self.context.aq_explicit
        blockconf = IBlockConfig(context)
        viewname = blockconf.viewname

        #ex. layout_name = 'listing'
        self.block_view = zope.component.queryMultiAdapter(
            (context, self.request), name='block_view-%s' % viewname)
        if not self.block_view:
            self.block_view = zope.component.queryMultiAdapter(
                (context, self.request), name='block_view')

        if self.block_view:
            return self.template()
        return self.render_fallback()


class SimpleLayoutAlignActionViewlet(ViewletBase):

    index = ViewPageTemplateFile('align_action.pt')

    def text(self):
        return self.context.restrictedTraverse(
            '@@sl_controls').ToggleGridLayoutText()

    def isTwoColumnLayout(self):
        context = aq_inner(self.context).aq_explicit

        if ISimplelayoutTwoColumnView.providedBy(context):
            return True
        if ISimplelayoutTwoColumnOneOnTopView.providedBy(context):
            return True
        return False
