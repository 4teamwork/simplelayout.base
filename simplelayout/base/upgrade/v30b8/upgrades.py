from plone.app.upgrade.utils import loadMigrationProfile


def hide_paragraph_from_search(context):
    """Change the storagetype of the imagefield for paragraph"""
    loadMigrationProfile(context, 'profile-simplelayout.base:v30b8')
