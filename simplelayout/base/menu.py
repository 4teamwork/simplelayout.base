from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import PloneMessageFactory as _
from Products.CMFPlone import utils
from plone.memoize.instance import memoize
from simplelayout.base.interfaces import ISlUtils, ISimpleLayoutCapable
from zope.component.hooks import getSite
from zope.browsermenu.menu import BrowserMenu
from zope.browsermenu.menu import BrowserSubMenuItem
from zope.browsermenu.interfaces import IBrowserMenu
from zope.browsermenu.interfaces import IBrowserSubMenuItem
from zope.component import getMultiAdapter
from zope.component import getUtility
from zope.interface import implements


class IBlockDesignSubMenu(IBrowserSubMenuItem):
    """The menu item linking to the help menu.
    """


class IBlockDesignMenu(IBrowserMenu):
    """The help menu
    """


class BlockDesignSubMenu(BrowserSubMenuItem):
    implements(IBlockDesignSubMenu)

    title = _(u'label_design_menu', default=u'Design')
    description = _(u'desc_design_menu',
                    default=u'change design of current page')
    submenuId = 'simplelayout_contentmenu_design'

    order = 5
    extra = {'id': 'simplelayout-contentmenu-design'}

    def __init__(self, context, request):
        BrowserSubMenuItem.__init__(self, context, request)
        self.context_state = getMultiAdapter((context, request),
                                             name='plone_context_state')

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

        context_state = getMultiAdapter((self.context, self.request),
                                        name=u'plone_context_state')
        sl_design_actions = context_state.actions().get(
            'object_simplelayout_designs', [])
        return len(sl_design_actions) > 0 and \
            conf.isDesignTabEnabled() and \
            ISimpleLayoutCapable.providedBy(self.context) and \
            conf.canMemberChangeDesign(self.context)

    def selected(self):
        return False


class BlockDesignMenu(BrowserMenu):
    implements(IBlockDesignMenu)

    def getMenuItems(self, context, request):
        """Return menu item entries in a TAL-friendly form."""
        results = []

        context_state = getMultiAdapter((context, request),
                                        name=u'plone_context_state')
        sl_design_actions = context_state.actions().get(
            'object_simplelayout_designs', [])

        if not sl_design_actions:
            return []

        for action in sl_design_actions:
            results.append({'title': action['title'],
                            'description': '',
                            'action': action['url'],
                            'selected': False,
                            'icon': None,
                            'extra': {'id': action['id'],
                                      'separator': None},
                            'submenu': None,
                            })

        return results
