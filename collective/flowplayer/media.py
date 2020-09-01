from persistent import Persistent

from zope.interface import implements
from zope.component import adapts

from collective.flowplayer.interfaces import IVideo, IMediaInfo


class VideoInfo(Persistent):
    implements(IMediaInfo)
    adapts(IVideo)

    def __init__(self):
        self.height = None
        self.width = None
        self.audio_only = False
