from zope.interface import implements
from zope.component import adapts
from zope.annotation.interfaces import IAnnotations
from simplelayout.base.interfaces import ISimpleLayoutBlock, IBlockConfig

class BlockConfig(object):

    
    implements(IBlockConfig)
    adapts(ISimpleLayoutBlock)

    def __init__(self, context):
        self.context = context
        self.annotations = IAnnotations(self.context)

    #stores the generated viewletManger name
    def get_viewlet_manager(self):
        return self.annotations.get('sl-viewlet', None)
    
    def set_viewlet_manager(self, value):
        if value:
            self.annotations['sl-viewlet'] = value 
            
    viewlet_manager = property(get_viewlet_manager, set_viewlet_manager)
            
    #stores the given layout
    def get_image_layout(self):
        return self.annotations.get('imageLayout', None)
    
    def set_image_layout(self, value):
        if value:
            self.annotations['imageLayout'] = value
            
    image_layout = property(get_image_layout, set_image_layout) 


    #stores the calculated imge dimension and scale    
    def get_image_scale(self):
        return self.annotations.get('scale', None)
    
    def set_image_scale(self,value):
        self.annotations['scale'] = value
        
    image_scale = property(get_image_scale, set_image_scale)
    
    def get_image_dimension(self):
        return self.annotations.get('dimension',None)
    
    def set_image_dimension(self, value):
        if value:
            self.annotations['dimension'] = value
            
    image_dimension = property(get_image_dimension, set_image_dimension)

            
    def get_block_height(self):
        return self.annotations.get('height',None)
    
    def set_block_height(self, value):
        self.annotations['height'] = value
            
    block_height = property(get_block_height, set_block_height)

    #stores the given viewname
    def get_viewname(self):
        return self.annotations.get('viewname', None)
    
    def set_viewname(self, value):
        self.annotations['viewname'] = value
            
    viewname = property(get_viewname, set_viewname)
