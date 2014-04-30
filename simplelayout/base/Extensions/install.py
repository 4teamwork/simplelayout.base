from Products.CMFCore.utils import getToolByName


PROJECTNAME = 'simplelayout.base'


def uninstall(self):
    setup_tool = getToolByName(self, 'portal_setup')
    setup_tool.runAllImportStepsFromProfile(
        'profile-{0}:uninstall'.format(PROJECTNAME),
        ignore_dependencies=True)
