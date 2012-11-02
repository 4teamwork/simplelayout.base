
from zope.i18nmessageid import MessageFactory
websiteMessageFactory = MessageFactory('simplelayout')


#init patches
from simplelayout.base.browser import patch_portletmanager
patch_portletmanager


def initialize(context):
    """Initializer called when used as a Zope 2 product."""
