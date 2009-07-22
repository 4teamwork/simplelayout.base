from zope.interface import Interface, Attribute
from zope.viewlet.interfaces import IViewletManager

class ISimpleLayoutLayer(Interface):
    """A layer specific to simplelayout
    """

class ISimpleLayoutCapable(Interface):
    """ marker interface"""

class ISimpleLayoutBlock(Interface):
    """ marker interface"""

class ISimpleViewletProvider(IViewletManager):
    """ marker interface"""
    
class ISimpleViewletListingProvider(IViewletManager):
    """ marker interface"""
    
class IBlockConfig(Interface):
    """
    """
    
class ISimpleLayoutListingViewlet(Interface):
    """Marker interface for the Listing Viewlet - it makes querying easier!
    """
class ISimpleLayoutListingTwoColumnsViewlet(Interface):
    """Marker interface for the 2 columns Listing Viewlet - it makes querying easier!
    """
class ISimpleLayoutListingTwoColumnsOneOnTopViewlet(Interface):
    """Marker interface for the 2 columns Listing Viewlet - it makes querying easier!
    """


class ISimplelayoutView(Interface):
    """base marker interface for simplelayout view
    """
    name = Attribute("""normal""")


class ISimplelayoutTwoColumnView(Interface):
    """base marker interface for simplelayout view
    """
    name = Attribute("""two-columns""")
    
class ISimplelayoutTwoColumnOneOnTopView(Interface):
    """base marker interface for simplelayout view
    """
    name = Attribute("""two-columns-one-on-top""")

class IScaleImage(Interface):
    """ marker interface """

class ISlUtils(Interface):
    """ marker interface for sl utils """



class ISlotA(Interface):
    """ This marker Interface descripes the slot to fill 
    """

class ISlotB(Interface):
    """ This marker Interface descripes the slot to fill 
    """
    
class ISlotC(Interface):
    """ This marker Interface descripes the slot to fill - no in use"""



class IOneColumn(Interface):
    """ This marker is for one Column Blocks 
    """

class ITwoColumn(Interface):
    """ TThis marker is for two Column Blocks 
    """
    
class IThreeColumn(Interface):
    """ This marker is for three Column Blocks - not in use"""
