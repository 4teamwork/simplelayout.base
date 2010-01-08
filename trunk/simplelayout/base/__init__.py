
from zope.i18nmessageid import MessageFactory
websiteMessageFactory = MessageFactory('simplelayout')

#init patches
import browser.patch_portletmanager

def initialize(context):
    """Initializer called when used as a Zope 2 product."""
