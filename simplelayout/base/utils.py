from Products.CMFCore.utils import getToolByName
from zope.interface import Interface
from zope.interface import implements
from simplelayout.base.config import BLOCK_INTERFACES, \
                                     COLUMN_INTERFACES_MAP, \
                                     IMAGE_SIZE_MAP_PER_INTERFACE, \
                                     CONFIGLET_INTERFACE_MAP
from simplelayout.base.interfaces  import IBlockConfig, IScaleImage
from simplelayout.base.configlet.interfaces import ISimplelayoutConfiguration
from zope.component import getUtility, queryUtility


class SlUtils(object):

    def isBlockWorkflowEnabled(self):
        conf = getUtility(ISimplelayoutConfiguration, name='sl-config')
        return conf.same_workflow

    def getSizeAttributesByInterface(self, content, size):
        #XXX get infos by a given value or by request
        current_iface = None
        for iface in COLUMN_INTERFACES_MAP.values():
            if iface.providedBy(content):
                current_iface = iface

        if current_iface is None:
            return size

        if current_iface in IMAGE_SIZE_MAP_PER_INTERFACE:
            return IMAGE_SIZE_MAP_PER_INTERFACE[current_iface][size]

        return size

    def isDesignTabEnabled(self):
        conf = getUtility(ISimplelayoutConfiguration, name='sl-config')
        return conf.show_design_tab

    def canMemberChangeDesign(self, context):
        conf = getUtility(ISimplelayoutConfiguration, name='sl-config')
        allowed_roles = conf.show_design_tab_roles
        if not allowed_roles:
            return True
        mt = getToolByName(context, 'portal_membership')
        member = mt.getAuthenticatedMember()
        #check if at least one list item is in the other list
        return len(set(allowed_roles.split('\n')).intersection(
                   set(member.getRolesInContext(context)))) > 0


class IBlockControl(Interface):
    """actions
    """

    def update(parent, block, request):
        """"""


class BaseBlockControl(object):
    implements(IBlockControl)

    def update(self, parent, block, request):
        self.block = block


class BlockActions(BaseBlockControl):

    def update(self, parent, block, request):
        self.block = block
        action = request.get('action', '')
        #XXX:
        if action == 'delete':
            parent.manage_delObjects(block.id)
        if action in ['moveup', 'movedo']:
            contents = parent.getFolderContents(
                {
                    'object_provides': BLOCK_INTERFACES,
                    'sort_order': 'getObjPositionInParent'})
            #get current blocks position
            ids = [content.id for content in contents]
            try:
                blockPosition = ids.index(block.id)
            except:
                blockPosition = 0
            if action in 'moveup' and blockPosition != 0:
                #XXX
                try:
                    upper = contents[blockPosition-1]
                    upperPosition= parent.getObjectPosition(upper.id)
                    parent.moveObjectToPosition(block.id, upperPosition)
                except:
                    pass
            if action == 'movedo':
                #XXX
                try:
                    lower = contents[blockPosition]
                    lowerPosition= parent.getObjectPosition(lower.id)
                    parent.moveObjectToPosition(block.id, lowerPosition+1)
                except:
                    pass
            parent.plone_utils.reindexOnReorder(parent)


class BlockLayout(BaseBlockControl):

    def update(self, parent, block, request, **kwargs):
        self.block = block
        #we store everything in annotations
        blockconf = IBlockConfig(block)
        layout = kwargs.get('layout', '')
        viewname = kwargs.get('viewname', '')
        if not layout:
            layout = request.get('layout', '')

        fieldname = request.get('fieldname', '')

        if not fieldname:
            fieldname = 'image'

        blockconf.image_layout = layout
        blockconf.viewname = viewname


class ImageScaler(object):
    implements(IScaleImage)

    def scaleMapper(self, content, scale):
        #maps an string to an integer value
        try:
            scale = int(scale)
            return scale
        except ValueError:
            pass

        #get data from configlets
        size_config = None
        #XXX hackish - use properties or try to make just one configlet
        for k in CONFIGLET_INTERFACE_MAP:
            #key is name of utility, value is the iface
            size_config = queryUtility(CONFIGLET_INTERFACE_MAP[k], name=k)
            if size_config:
                try:
                    mapper = {
                        'small': getattr(
                            size_config,
                            SlUtils().getSizeAttributesByInterface(
                                content,
                                'small_size')),
                        'middle': getattr(
                            size_config,
                            SlUtils().getSizeAttributesByInterface(
                            content,
                            'middle_size')),
                        'full': getattr(
                            size_config,
                            SlUtils().getSizeAttributesByInterface(
                            content,
                            'full_size')),
                        'no-image': 0}
                except AttributeError:
                    continue

        if scale in mapper.keys():
            return mapper[scale]
        else:
            #damit...no scale found
            return 0

    def get_image_attributes(self, content):
        """Returns a dict with image attributes, like width and height.
        currently we are only interesst in height

        """
        # get the stored layout
        blockconf = IBlockConfig(content)
        #layout contains the image size and also an aditional css class
        image_layout = str(blockconf.image_layout).split('-')
        layout = len(image_layout) != 0 and image_layout[0] or None

        #check for img_width
        if layout is None:
            return dict(width = 0, height = 0)
        img_width = self.scaleMapper(content, layout)

        # calc img height depending on our width
        field = content.getField('image')
        if field:
            img = field.getRaw(content)
        else:
            return dict(width = 0, height = 0)
            
        # jump out if img is empty or there's a bitmap
        if img == '' or img is None or img.content_type == 'image/x-ms-bmp':
            return dict(width = 0, height = 0)

        orig_img_width = img.width
        orig_img_height = img.height
        img_height = int(img_width*
            (float(orig_img_height)/
            float(orig_img_width)))

        return dict(
            width = img_width,
            height = img_height)
