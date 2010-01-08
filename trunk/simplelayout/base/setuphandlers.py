from StringIO import StringIO
from zope.component import queryUtility, provideUtility
from Products.CMFCore.utils import getToolByName
from zope.component import getSiteManager

from simplelayout.base.configlet.interfaces import ISimplelayoutConfiguration
from simplelayout.base.configlet.view import SimpleLayoutConfiguration

# register local utility
def registerLocalUtility(context):
    portal = context.getSite()
    sm = getSiteManager(portal)
    
    ###use component registry
    
    #if not sm.queryUtility(ISimplelayoutConfiguration, name='sl-config'):
    #     sm.registerUtility(SimpleLayoutConfiguration(),
    #                        ISimplelayoutConfiguration,
    #                        'sl-config')

def reorderJS(context):
    """
    reorders js the right way
    """
    portal = context.getSite()
    js_reg = portal.portal_javascripts
    
    # we can do this now by GS
    """
    try:
        js_reg.moveResourceBefore('++resource++simplelayout.ui.base-resources/jq-QueuManagerPlugin-v0.2.js', '++resource++sl/simplelayout.js')
        js_reg.moveResourceBefore('++resource++simplelayout.ui.dragndrop-resources/jquery-ui-current.js', '++resource++sl/simplelayout.js')
        js_reg.moveResourceBefore('++resource++sl/pxem_Jqueryplugin.js', '++resource++sl/simplelayout.js')
        js_reg.moveResourceAfter('++resource++simplelayout.ui.base-resources/sl-base.js', '++resource++sl/simplelayout.js')
        js_reg.moveResourceAfter('sl_ui_variables.js', '++resource++simplelayout.ui.base-resources/sl-base.js')
        js_reg.moveResourceAfter('++resource++simplelayout.ui.dragndrop-resources/sl-dnd-reorder.js', 'sl_ui_variables.js')
    except ValueError:
        pass
    """
