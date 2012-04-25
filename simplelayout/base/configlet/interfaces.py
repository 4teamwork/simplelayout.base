from zope.interface import Interface
from zope import schema

from simplelayout.base import websiteMessageFactory as _

class ISimplelayoutConfiguration(Interface):
    """This interface defines the configlet with basic configuration."""

                                                          
    same_workflow = schema.Bool(title=_(u'paragraph has workflow'),
                                description=_(u'Decide if Paragraphs can have their own workflow'),
                                default=False)
                                
    show_design_tab = schema.Bool(title=_(u"Show Design"),
                                description=_(u'If enabled it is possible to change between 2 or more designs, ex. a two column design'),
                                default=True)

    show_design_tab_roles = schema.Text(
        title=_(u'Limit design for roles'),
        description=_(u'Enter roles which can change the designs. Ignores if nothing is specified. One per line.'),
        required=False,
        default=u'',
    )

class ISimplelayoutConfigurationOneColumn(Interface):
    """This interface defines the one column conf."""
    small_size = schema.Int(title=_(u'Small size one column'),
                            description=_(u'enter value (px)'),
                            default= 250,
                            required=True) 

    middle_size = schema.Int(title=_(u"Middle size one column"),
                            description=_(u'enter value (px)'),
                            default= 500,
                            required=True) 

    full_size = schema.Int(title=_(u"Full/big size one column"),
                            description=_(u'enter value (px)'),
                            default= 1000,
                            required=True) 
                            
class ISimplelayoutConfigurationTwoColumn(Interface):
    """This interface defines the two column conf."""

    small_size_two = schema.Int(title=_(u"Small size two column"),
                            description=_(u'enter value (px)'),
                            default= 250,
                            required=True) 

    middle_size_two = schema.Int(title=_(u"Middle size two column"),
                            description=_(u'enter value (px)'),
                            default= 500,
                            required=True) 

    full_size_two = schema.Int(title=_(u"Full/big size two column"),
                            description=_(u'enter value (px)'),
                            default= 1000,
                            required=True) 
