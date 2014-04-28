from Products.CMFCore.utils import getToolByName


def registerLocalUtility(context):
    # XXX remove this import step with an upgrade step, since
    # the import step registration is persistent (import_steps.xml).
    # The registration is done in componentregistry.xml
    return


def reorderJS(context):
    # XXX remove this import step with an upgrade step, since
    # the import step registration is persistent (import_steps.xml).
    # The reordering is done with generic setup.
    return


def import_various(context):
    portal = context.getSite()
    action = context.readDataFile('simplelayout.base.various.txt')
    action = action.strip() if action else None

    if action == 'uninstall':
        uninstall_controlpanel(portal)


def uninstall_controlpanel(portal):
    controlpanel = getToolByName(portal, 'portal_controlpanel')
    controlpanel.unregisterConfiglet('simplelayout-configuration')
