from simplelayout.base.interfaces import ISimplelayoutView, \
                                         ISimplelayoutTwoColumnView, \
                                         ISimplelayoutTwoColumnOneOnTopView, \
                                         ISlotA, ISlotB, ISlotC, \
                                         IOneColumn,ITwoColumn,IThreeColumn

from simplelayout.base.configlet.interfaces import ISimplelayoutConfiguration

BLOCK_INTERFACES = [
                    'simplelayout.base.interfaces.ISimpleLayoutBlock',
                    ]

VIEW_INTERFACES_MAP = {
                       'normal':ISimplelayoutView,
                       'two-columns':ISimplelayoutTwoColumnView, 
                       'two-columns-one-on-top':ISimplelayoutTwoColumnOneOnTopView
                      }

SLOT_INTERFACES_MAP = {
                       'slotA' : ISlotA, 
                       'slotB' : ISlotB,
                       'slotC' : ISlotC
                       }

COLUMN_INTERFACES_MAP = {
                       'onecolumn' : IOneColumn, 
                       'twocolumn' : ITwoColumn,
                       'threecolumn' : IThreeColumn
                       }
                       
INIT_INTERFACES_MAP = {
                       'normal' : [ISlotA, IOneColumn],
                       'two-columns': [ISlotA, ITwoColumn],
                       'two-columns-one-on-top' : [ISlotA, IOneColumn]
                      }
                      
IMAGE_SIZE_MAP_PER_INTERFACE = {
                                IOneColumn : dict(small_size = 'small_size', 
                                                  middle_size = 'middle_size',
                                                  full_size = 'full_size'), 
                                ITwoColumn : dict(small_size = 'small_size_two',
                                                  middle_size ='middle_size_two',
                                                  full_size = 'full_size_two'), 
                                } 

# take a look at componentregistry.xml
# key = utility name, value = interface
CONFIGLET_INTERFACE_MAP = {
                           'sl-config': ISimplelayoutConfiguration,
                           }
